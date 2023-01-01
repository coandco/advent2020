from utils import read_data
import re


class Rule:
    def __init__(self, line):
        self.low, self.high, self.char, _, self.password = re.split("[ :-]", line)
        self.low = int(self.low)
        self.high = int(self.high)


def main():
    rules = [Rule(line) for line in read_data().split("\n")]
    num_valid = 0
    for rule in rules:
        num_in_pass = rule.password.count(rule.char)
        if rule.low <= num_in_pass <= rule.high:
            num_valid += 1
    print(f"Part one: {num_valid}")

    num_valid = 0
    for rule in rules:
        needed_chars = rule.password[rule.low-1] + rule.password[rule.high-1]
        if needed_chars.count(rule.char) == 1:
            num_valid += 1

    print(f"Part two: {num_valid}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")

