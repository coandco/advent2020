from utils import read_data
from typing import List, Tuple, Dict, NamedTuple


class BusInfo(NamedTuple):
    interval: int
    offset: int

    def valid_part_one(self, time: int) -> bool:
        return time % self.interval == 0

    def valid_part_two(self, time: int) -> bool:
        return ((time + self.offset) % self.interval) == 0


def part_one(earliest_time: int, bus_list: List[BusInfo]) -> Tuple[int, int]:
    current_time = earliest_time
    # Iterate forward in time until you get at least one valid bus
    while True:
        arrived_buses = [x for x in bus_list if x.valid_part_one(current_time)]
        if arrived_buses:
            break
        current_time += 1
    return arrived_buses[0].interval, current_time - earliest_time


def get_new_step(bus: BusInfo, start_time: int = 0, existing_step: int = 1) -> Tuple[int, int]:
    times = []
    # Iterate through times, starting at start_time and stepping by existing_step,
    # until you find the next two instances where the bus is valid.  Return the
    # first instance as the new start value and the difference as the new interval.
    current_time = start_time
    while True:
        if bus.valid_part_two(current_time):
            times.append(current_time)
            if len(times) == 2:
                new_start_time = times[0]
                new_step_value = times[1] - times[0]
                return new_start_time, new_step_value
        current_time += existing_step


# For debug purposes to check the state at a particular time
# Returns a dict of {bus_id: bool}, where bool is if the bus is valid for the particular timestamp
def check_buses_at_time(bus_list: List[BusInfo], time_to_check: int) -> Dict[int, bool]:
    return {x.interval: x.valid_part_two(time_to_check) for x in bus_list}


def part_two(bus_list: List[BusInfo]) -> int:
    current_step = 1
    start_time = 0
    # For each bus, find the next time that this bus is valid, and the interval to step at for it to be always valid
    #
    # Then do it again with the next bus, using the start/step from the previous iteration to ensure that
    # all previous buses stay valid
    for bus in bus_list:
        start_time, current_step = get_new_step(bus, start_time, current_step)
        #print(f"Bus status at time {start_time}: {check_buses_at_time(bus_list, start_time)}")
    # When you've gone through all of the buses in the list, you arrive at a start_time where all of them are valid
    return start_time


def main():
    schedule_card = read_data().split("\n")
    part_one_start_time = int(schedule_card[0])
    # Make a sorted list of BusInfo NamedTuples, with the highest interval first
    buslist = sorted([BusInfo(offset=i, interval=int(busname))
                      for i, busname in enumerate(schedule_card[1].split(",")) if busname != "x"],
                     reverse=True)
    first_bus, time_diff = part_one(part_one_start_time, buslist)
    print(f"Part one: {first_bus * time_diff}")
    print(f"Part two: {part_two(buslist)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
