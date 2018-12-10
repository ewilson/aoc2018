import re

from common import readfile

class MovingPoint:

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, forward = 1):
        self.x += forward * self.dx
        self.y += forward * self.dy

    def __repr__(self):
        return f'({self.x}, {self.y}) -- ({self.dx}, {self.dy})'


def transformer(line):
    nl = line.replace('velocity=', '').replace('position=', '')
    split_line = re.split('[<>, ]+', nl)
    return MovingPoint(int(split_line[1]), int(split_line[2]), int(split_line[3]), int(split_line[4]))


def max_dim(data):
    max_x, min_x, max_y, min_y = None, None, None, None
    for d in data:
        if max_x is None or d.x > max_x:
            max_x = d.x
        if min_x is None or d.x < min_x:
            min_x = d.x
        if max_y is None or d.y > max_y:
            max_y = d.y
        if min_y is None or d.y < min_y:
            min_y = d.y
    return max_x, min_x, max_y, min_y


def back_up(data):
    for d in data:
        d.move(-1)

def go(data):
    for d in data:
        d.move()


def solve(data):
    prev_dim = max_dim(data)
    prev_area = (prev_dim[0] - prev_dim[1]) * (prev_dim[2] - prev_dim[3])
    print_it = False
    while True:
        for d in data:
            d.move()
        cur_dim = max_dim(data)
        if abs(cur_dim[2] - cur_dim[3]) < 15:
            print_it = True
        if print_it:
            input('ready')
            print_data(data)
            break

        # cur_area = (cur_dim[0] - cur_dim[1]) * (cur_dim[2] - cur_dim[3])
        #
        # if cur_area > prev_area:
        #     break
        # prev_area = cur_area
        # print(cur_dim)


def print_data(data):

    dims = max_dim(data)
    print(dims)
    for y in range(dims[3], dims[2] + 1):
        pound = 0
        space = 0
        for x in range(dims[1], dims[0] + 1):
            point = False
            for d in data:
                if d.x == x and d.y == y:
                    print('#', end='')
                    pound += 1
                    point = True
                    break
            if not point:
                space += 1
                print(' ', end='')
        print(f'next: {x} -- {pound + space}')


def get_test_data():
    return readfile('d10/test.txt', transformer)


def get_real_data():
    return readfile('d10/data.txt', transformer)
