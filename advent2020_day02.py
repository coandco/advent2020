from utils import read_data

INPUT = read_data().split("\n")

num_valid = 0
for line in INPUT:
    numbers, char, password = line.split(" ")
    low, high = numbers.split("-")
    char = char[0]
    num_in_pass = password.count(char)
    if int(low) <= num_in_pass <= int(high):
        num_valid += 1

print(f"Part one: {num_valid}")
num_valid = 0
for line in INPUT:
    numbers, char, password = line.split(" ")
    low, high = numbers.split("-")
    char = char[0]
    needed_chars = password[int(low)-1] + password[int(high)-1]
    if needed_chars.count(char) == 1:
        num_valid += 1

print(f"Part two: {num_valid}")
