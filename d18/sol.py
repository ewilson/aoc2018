from common import readfile


def get_test_data():
    return readfile('d18/test.txt', list)


def get_real_data():
    return readfile('d18/data.txt', list)


class World:

    def __init__(self, array):
        self.tuple = tuple(tuple(el for el in row) for row in array)
        self.width = len(array[0])
        self.height = len(array)

    def iterate(self):
        new_array = []
        for j, row in enumerate(self.tuple):
            new_array.append(['']*self.width)
            for i, el in enumerate(row):
                new_array[j][i] = self.generate(el, i, j)
        self.tuple = tuple(tuple(el for el in row) for row in new_array)

    def iter_n(self, n):
        for _ in range(n):
            self.iterate()

    def _inside_dims(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    def generate(self, el, x, y):
        neighbor_coords = [(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2) if self._inside_dims(i, j) and not (i, j) == (x, y)]
        neighbors = [self.tuple[y][x] for (x, y) in neighbor_coords]
        if self.tuple[y][x] == '.':
            next_state = '|' if neighbors.count('|') >= 3 else '.'
        elif self.tuple[y][x] == '|':
            next_state = '#' if neighbors.count('#') >= 3 else '|'
        elif self.tuple[y][x] == '#':
            next_state = '.' if neighbors.count('#') == 0 or neighbors.count('|') == 0 else '#'
        return next_state

    def resource_value(self):
        tc, lc = 0, 0
        for row in self.tuple:
            for el in row:
                if el in '|':
                    tc += 1
                elif el in '#':
                    lc += 1
        return tc * lc

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __hash__(self):
        return hash(self.tuple)

    def __repr__(self):
        return '\n'.join([''.join([el for el in row]) for row in self.tuple])


def solve(data):
    d = {}
    m = 0
    w = World(data)
    while hash(w) not in d:
        d[hash(w)] = m
        w.iterate()
        m += 1
    print(w)
    print(m)
    print(d[hash(w)])
    return w
