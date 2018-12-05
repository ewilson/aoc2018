from string import ascii_lowercase

from common import readfile

TEST_DATA = True


def match(left, right):
    return left != right and left.lower() == right.lower()


def react(data, discard = ''):
    stack = []
    for element in data:
        if element.lower() == discard:
            continue
        if not stack or not match(element, stack[-1]):
            stack.append(element)
        else:
            stack.pop()
    return ''.join(stack)


def solve(test_data=TEST_DATA):
    filename = 'd05/test.txt' if test_data else 'd05/data.txt'
    data = readfile(filename, list)[0]
    result_dict = {}
    for letter in ascii_lowercase:
        result_dict[letter] = react(data, letter)

    shortest = min(result_dict.values(), key=len)

    return shortest