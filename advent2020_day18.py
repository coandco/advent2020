from utils import read_data
from typing import Tuple, Dict


def find_matching_parens(text: str) -> Dict[int, int]:
    paren_stack = []  # stack of indices of opening parentheses
    parens_dict = {}

    for i, char in enumerate(text):
        if char == '(':
            paren_stack.append(i)
        if char == ')':
            try:
                parens_dict[paren_stack.pop()] = i
            except IndexError:
                raise Exception("Couldn't parse parens because there are too many closing parenthesis")
    if paren_stack:  # check if stack is empty afterwards
        raise Exception("Couldn't parse parens because there are too many opening parentheses")
    return parens_dict


OP_DICT = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y
}


def evaluate_part_one(expression: str) -> int:
    expression = expression.replace(" ", "")
    parens_dict = find_matching_parens(expression)
    index = 0
    stored_number = None
    stored_op = None
    while index < len(expression):
        char = expression[index]
        if char.isnumeric():
            if stored_number is not None and stored_op is not None:
                stored_number = OP_DICT[stored_op](stored_number, int(char))
                stored_op = None
            elif stored_number is not None and stored_op is None:
                raise Exception("Read two numbers in a row, what do?")
            elif stored_number is None:
                stored_number = int(char)
            index += 1
        elif char in ('+', '*'):
            if stored_op is None:
                stored_op = char
            else:
                raise Exception("Read two ops in a row, what do?")
            index += 1
        elif char == '(':
            sub_problem = expression[index+1:parens_dict[index]]
            sub_value = evaluate_part_one(sub_problem)
            if stored_number is not None and stored_op is not None:
                stored_number = OP_DICT[stored_op](stored_number, sub_value)
                stored_op = None
            elif stored_number is not None and stored_op is None:
                raise Exception("Read two numbers in a row, what do?")
            elif stored_number is None:
                stored_number = sub_value
            index = parens_dict[index]+1
    return stored_number


def get_left_num(expression: str, index: int) -> Tuple[int, int]:
    num_start = index
    while num_start - 1 >= 0 and expression[num_start - 1].isnumeric():
        num_start -= 1
    return int(expression[num_start:index]), num_start


def get_right_num(expression: str, index: int) -> Tuple[int, int]:
    num_end = index
    while num_end + 1 < len(expression) and expression[num_end+1].isnumeric():
        num_end += 1
    return int(expression[index+1:num_end+1]), num_end


def evaluate_part_two(expression: str) -> int:
    expression = expression.replace(" ", "")
    while '(' in expression:
        parens = find_matching_parens(expression)
        first_paren = min(parens.keys())
        sub_problem = expression[first_paren + 1:parens[first_paren]]
        sub_value = evaluate_part_two(sub_problem)
        expression = str(sub_value).join((expression[:first_paren], expression[parens[first_paren]+1:]))
    while '+' in expression:
        plus_loc = expression.index("+")
        left_num, left_num_start = get_left_num(expression, plus_loc)
        right_num, right_num_end = get_right_num(expression, plus_loc)
        expression = str(left_num+right_num).join((expression[:left_num_start], expression[right_num_end+1:]))
    while '*' in expression:
        mult_loc = expression.index("*")
        left_num, left_num_start = get_left_num(expression, mult_loc)
        right_num, right_num_end = get_right_num(expression, mult_loc)
        expression = str(left_num * right_num).join((expression[:left_num_start], expression[right_num_end + 1:]))
    return int(expression)


def main():
    expressions = read_data().split("\n")
    print(f'Part one: {sum(evaluate_part_one(line) for line in expressions)}')
    print(f"Part two: {sum(evaluate_part_two(line) for line in expressions)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
