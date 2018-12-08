from common import readfile
from collections import defaultdict

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def transformer(line):
    x, y = line.split(',')
    return int(x), int(y)


def full_grid(data, x_min, x_max, y_min, y_max):
    grid = {}
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            min_dist = None
            nearest_pt = None
            for p in data:
                d = dist(p, (i,j))
                if min_dist is None or d < min_dist:
                    min_dist = d
                    nearest_pt = p
                elif d == min_dist:
                    nearest_pt = None
            grid[(i, j)] = min_dist, nearest_pt
    return grid


def add_them(closest_data, x_min, x_max, y_min, y_max):
    sums = defaultdict(int)
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            nearest_pt = closest_data[(i, j)][1]
            if nearest_pt is not None:
                sums[nearest_pt] += 1
    return sums


def solve(test_data):
    filename = 'd06/data.txt' if test_data else 'd06/test.txt'
    data = readfile(filename, transformer)
    x_min = min(data, key=lambda p: p[0])[0]
    x_max = max(data, key=lambda p: p[0])[0]
    y_min = min(data, key=lambda p: p[1])[1]
    y_max = max(data, key=lambda p: p[1])[1]

    finite = part1(data, x_max, x_min, y_max, y_min)

    return part2(data, x_max, x_min, y_max, y_min)
    # return max(finite.values())


def part2(data, x_max, x_min, y_max, y_min):
    grid = defaultdict(int)
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            for p in data:
                grid[(i, j)] += dist(p, (i,j))
    return len({p: grid[p] for p in grid if grid[p] < 10000})
    # return grid


def part1(data, x_max, x_min, y_max, y_min):
    closest_data = full_grid(data, x_min - 1, x_max + 1, y_min - 1, y_max + 1)
    points_nearby = add_them(closest_data, x_min, x_max, y_min, y_max)
    extra_points_nearby = add_them(closest_data, x_min - 1, x_max + 1, y_min - 1, y_max + 1)
    finite = {p: points_nearby[p] for p in points_nearby if extra_points_nearby[p] == points_nearby[p]}
    return finite


def test():
    return solve(False)


def answer():
    return solve(True)
