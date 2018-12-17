from common import readfile

test = '''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
'''


def get_test_data():
    return [list(line) for line in test.splitlines()]


def get_data():
    return readfile('d15/data.txt', transformer=list)


