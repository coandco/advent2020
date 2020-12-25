from utils import read_data
from typing import List


def transform_subject(subject_number: int, current_value: int = 1):
    current_value *= subject_number
    current_value %= 20201227
    return current_value


def find_loop_size(public_key: int, subject_number: int = 7) -> int:
    current_value = 1
    for i in range(1, 99999999):
        current_value = transform_subject(subject_number, current_value)
        if current_value == public_key:
            return i


def get_key(data: List[str]) -> int:
    card_key, door_key = (int(x) for x in data)
    card_loop_size = find_loop_size(card_key)
    print(f"Card loop size is {card_loop_size}")
    door_loop_size = find_loop_size(door_key)
    print(f"Door loop size is {door_loop_size}")
    card_encryption = 1
    for _ in range(card_loop_size):
        card_encryption = transform_subject(door_key, card_encryption)
    door_encryption = 1
    for _ in range(door_loop_size):
        door_encryption = transform_subject(card_key, door_encryption)
    assert card_encryption == door_encryption
    return card_encryption


if __name__ == '__main__':
    print(get_key(read_data().split("\n")))
