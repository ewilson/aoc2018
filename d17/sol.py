import re

from common import readfile


def transformer(line):
    pattern = r'(\w)=(\d+),\s+(\w)=(\d+)\.\.(\d+)'
    m = re.match(pattern, line)
    if m.group(1) == 'x' and m.group(3) == 'y':
        return [(int(m.group(2)), y) for y in range(int(m.group(4)), int(m.group(5)) + 1)]
    elif m.group(1) == 'y' and m.group(3) == 'x':
        return [(x, int(m.group(2))) for x in range(int(m.group(4)), int(m.group(5)) + 1)]
    else:
        return 'ERROR'


def get_test_data():
    return readfile('d17/test.txt', transformer=transformer)


def get_real_data():
    return readfile('d17/data.txt', transformer=transformer)


class Ground:

    def __init__(self, clay):
        self.min_x = min([x for x, _ in clay]) - 1
        self.max_x = max([x for x, _ in clay]) + 1
        self.max_y = max([y for _, y in clay])
        self.ground = {(x, y): '#' for x, y in clay}
        self.ground[(500, 0)] = '+'
        self.active_flow = [(500, 0)]

    def _dry_sand(self, tile):
        return tile not in self.ground and tile[1] <= self.max_y

    def _below(self, tile):
        return tile[0], tile[1] + 1

    def _above(self, tile):
        return tile[0], tile[1] - 1

    def _left(self, tile):
        return tile[0]-1, tile[1]

    def _right(self, tile):
        return tile[0]+1, tile[1]

    def _settle(self, left, right):
        current = left
        while current != self._right(right):
            self.ground[current] = '~'
            current = self._right(current)

    def flow_n(self, n):
        for _ in range(n):
            self.flow()

    def flow(self):
        stream = self.active_flow.pop()
        below = self._below(stream)
        if self._dry_sand(below):
            self.ground[below] = '|'
            self.active_flow.append(below)
        elif self.ground[below] in '#~':
            self._go_sideways(stream)

    def _go_sideways(self, stream):
        left_barrier, right_barrier = False, False
        left_escape, right_escape = False, False
        left_flow = stream
        right_flow = stream
        while not (left_barrier or left_escape) or not (right_barrier or right_escape):
            if self._dry_sand(self._left(left_flow)):
                left_flow = self._left(left_flow)
                if self._dry_sand(self._below(left_flow)):
                    self.active_flow.append(self._below(left_flow))
                    left_escape = True
            elif self.ground[self._left(left_flow)] == '#':
                left_barrier = True
            if self._dry_sand(self._right(right_flow)):
                right_flow = self._right(right_flow)
                if self._dry_sand(self._below(right_flow)):
                    self.active_flow.append(self._below(right_flow))
                    right_escape = True
            elif self.ground[self._right(right_flow)] == '#':
                right_barrier = True
        if left_barrier and right_barrier:
            self._settle(left_flow, right_flow)
            self.active_flow.append(self._above(stream))
        if left_escape:
            self.active_flow.append(left_flow)
        if right_escape:
            self.active_flow.append(right_flow)

    def _tile(self, x, y):
        if (x, y) in self.ground:
            return self.ground[(x, y)]
        else:
            return '.'

    def __repr__(self):
        return '\n'.join([''.join([self._tile(x, y) for x in range(self.min_x, self.max_x + 1)]) for y in range(0, self.max_y + 1)])


def solve(data):
    clay_points = set()
    for vein in data:
        clay_points.update(vein)
    return Ground(clay_points)
