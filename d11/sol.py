from collections import defaultdict


def power_level(x, y, serialId):
    rack_id = x + 10
    init_val = rack_id * y
    level = init_val + serialId
    level *= rack_id
    hundreds = (level % 1000) // 100
    return hundreds - 5


def build_grid(width, height, serial_idd):
    grid = defaultdict(int)
    for y in range(height):
        for x in range(width):
            grid[(x,y)] = power_level(x, y, serial_idd)
    return grid


def sum9(x, y, grid):
    total = 0
    for i in range(x, x + 3):
        for j in range(y, y + 3):
            total += grid[(i, j)]
    return total


def solve(serial_idd):
    vals = defaultdict(int)
    grid = build_grid(300, 300, serial_idd)
    for x in range(1, 299):
        for y in range(1, 299):
            vals[(x,y)] = sum9(x, y, grid)
    return max(vals, key=vals.get)

