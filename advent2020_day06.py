from utils import read_data
from typing import List


class Group:
    def __init__(self, group_lines: List[str]):
        self.records = []
        for line in group_lines:
            self.records.append(set(line))
        self.any_questions_answered = set.union(*self.records)
        self.all_questions_answered = set.intersection(*self.records)


parsed_groups = [Group(x.split("\n")) for x in read_data().split("\n\n")]
print(f"Part one: {sum(len(x.any_questions_answered) for x in parsed_groups)}")
print(f"Part two: {sum(len(x.all_questions_answered) for x in parsed_groups)}")
