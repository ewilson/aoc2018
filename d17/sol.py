import re

from common import readfile


def transformer(line):
    pattern = r'(\w)=(\d+),\s+(\w)=(\d+)\.\.(\d+)'
    m = re.match(pattern, line)
    if m.group(1) == 'x' and m.group(3) == 'y':
        return [(m.group(2), y) for y in range(int(m.group(4)), int(m.group(5)) + 1)]
    elif m.group(1) == 'y' and m.group(3) == 'x':
        return [(x, m.group(2)) for x in range(int(m.group(4)), int(m.group(5)) + 1)]
    else:
        return 'ERROR'


def get_test_data():
    return readfile('d17/test.txt', transformer=transformer)


def get_real_data():
    return readfile('d17/data.txt', transformer=transformer)


def solve(data):
    clay_points = set()
    for vein in data:
        clay_points.update(vein)
    return clay_points
