from utils import read_data
from typing import List, Tuple, Dict, NamedTuple
import sys


class BusInfo(NamedTuple):
    interval: int
    offset: int

    def valid_at_time(self, time: int) -> bool:
        return (time + self.offset) % self.interval == 0


def part_one(earliest_time: int, bus_list: List[BusInfo]) -> Tuple[int, int]:
    current_time = earliest_time
    # Iterate forward in time until you get at least one valid bus
    while True:
        arrived_buses = [x for x in bus_list if x.valid_at_time(current_time)]
        if arrived_buses:
            break
        current_time += 1
    return arrived_buses[0].interval, current_time - earliest_time


def get_new_step(bus: BusInfo, start_time: int = 0, existing_step: int = 1) -> Tuple[int, int]:
    times = []
    # Iterate through times, starting at start_time and stepping by existing_step,
    # until you find the next two instances where the bus is valid.  Return the
    # first instance as the new start value and the difference as the new interval.
    for i in range(start_time, sys.maxsize, existing_step):
        if bus.valid_at_time(i):
            times.append(i)
            if len(times) == 2:
                new_start_time = times[0]
                new_step_value = times[1] - times[0]
                return new_start_time, new_step_value


# For debug purposes to check the state at a particular time
# Returns a dict of {bus_id: bool}, where bool is if the bus is valid for the particular timestamp
def check_buses_at_time(bus_list: List[BusInfo], time_to_check: int) -> Dict[int, bool]:
    return {x.interval: x.valid_at_time(time_to_check) for x in bus_list}


def part_two(bus_list: List[BusInfo]) -> int:
    current_step = 1
    start_time = 0
    # For each bus, find the next time that this bus is valid, and the interval to step at for it to be always valid
    #
    # Then do it again with the next bus, using the start/step from the previous iteration to ensure that
    # all previous buses stay valid
    for bus in bus_list:
        start_time, current_step = get_new_step(bus, start_time, current_step)
        print(f"Bus status at time {start_time}: {check_buses_at_time(buslist, start_time)}")
    # When you've gone through all of the buses in the list, you arrive at a start_time where all of them are valid
    return start_time


INPUT = read_data().split("\n")
part_one_start_time = int(INPUT[0])
# Make a sorted list of BusInfo NamedTuples, with the highest interval first
buslist = sorted([BusInfo(offset=i, interval=int(busname))
                  for i, busname in enumerate(INPUT[1].split(",")) if busname != "x"],
                 reverse=True)
first_bus, time_diff = part_one(part_one_start_time, buslist)
print(f"Bus {first_bus} arrives {time_diff} minutes past the start time, for a result of {first_bus * time_diff}")
print(f"The earliest timestamp that all of the buses sync up at is {part_two(buslist)}")

