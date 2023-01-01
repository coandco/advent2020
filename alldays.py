from importlib import import_module
import time

times = []
for i in range(1, 26):
    print(f"-----DAY {i}-----")
    try:
        day = import_module(f"advent2020_day{i:02}")
    except ModuleNotFoundError:
        break
    day_start = time.monotonic()
    day.main()
    times.append(time.monotonic()-day_start)
print("Individual days:")
print("\n".join(f"Day {i}: {x}" for i, x in enumerate(times, start=1)))
print(f"Time for all days: {sum(times)}")
