from utils import read_data
from typing import List, Dict
import re

NEEDED_FIELDS = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
}

EYE_COLORS = {
    "amb",
    "blu",
    "brn",
    "gry",
    "grn",
    "hzl",
    "oth"
}


def parse_data(input_data: str) -> List[Dict[str, str]]:
    data = input_data.split("\n\n")
    intermediate = [re.split(r'[\n ]', x) for x in data]
    final = []
    for record in intermediate:
        record_dict = {}
        for item in record:
            key, value = item.split(":")
            record_dict[key] = value
        final.append(record_dict)
    return final


def all_fields_valid(record: Dict[str, str]) -> bool:
    for key, value in record.items():
        if key == "byr":
            if len(value) != 4 or not (1920 <= int(value) <= 2002):
                return False
        elif key == "iyr":
            if len(value) != 4 or not (2010 <= int(value) <= 2020):
                return False
        elif key == "eyr":
            if len(value) != 4 or not (2020 <= int(value) <= 2030):
                return False
        elif key == "hgt":
            if value.endswith("cm"):
                if not (150 <= int(value[:-2]) <= 193):
                    return False
            elif value.endswith("in"):
                if not (59 <= int(value[:-2]) <= 76):
                    return False
            else:
                return False
        elif key == "hcl":
            if len(value) != 7 or not value.startswith("#"):
                return False
            try:
                int(value[1:], base=16)
            except ValueError:
                return False
        elif key == "ecl":
            if value not in EYE_COLORS:
                return False
        elif key == "pid":
            if len(value) != 9 or not value.isnumeric():
                return False
    return True


def main():
    parsed_data = parse_data(read_data())

    total_valid = 0
    for record in parsed_data:
        if NEEDED_FIELDS.issubset(record.keys()):
            total_valid += 1

    print(f"Part one: {total_valid}")

    total_valid = 0
    for record in parsed_data:
        if NEEDED_FIELDS.issubset(record.keys()) and all_fields_valid(record):
            total_valid += 1

    print(f"Part two: {total_valid}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
