def readfile(filename):
    return [list(s) for s in open(filename).readlines()]


def get_test_data():
    return readfile('d13/test.txt')


def get_real_data():
    return readfile('d13/data.txt')


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tuple = x, y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


EAST = 0
NORTH = 1
WEST = 2
SOUTH = 3

RIGHT = -1
STRAIGHT = 0
LEFT = 1

DIRECTION_VECTOR = [Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]

curves = {
    (NORTH, '\\'): WEST,
    (NORTH, '/'): EAST,
    (SOUTH, '\\'): EAST,
    (SOUTH, '/'): WEST,
    (EAST, '\\'): SOUTH,
    (EAST, '/'): NORTH,
    (WEST, '\\'): NORTH,
    (WEST, '/'): SOUTH,
}


class Location:

    def __init__(self, point, road, grid, occupied=False):
        self.point = point
        self.road = road
        self.occupied = occupied
        self.neighbors = []
        self.grid = grid

    def next(self, direction):
        return self.grid[(self.point + DIRECTION_VECTOR[direction]).tuple]

    def __repr__(self):
        return f'({self.point.x}, {self.point.y})'


class Cart:

    def __init__(self, direction, location):
        self.direction = direction
        self.location = location
        self.intersection = LEFT

    def move(self):
        self.location.occupied = False
        self.location = self.location.next(self.direction)
        if self.location.occupied:
            return self.location
        else:
            self.location.occupied = True
        if self.location.road in ['\\', '/']:
            self.direction = curves[(self.direction, self.location.road)]
        elif self.location.road == '+':
            self.direction = (self.direction + self.intersection) % 4
            self.intersection = self.intersection - 1 if self.intersection > RIGHT else self.intersection + 2

    @property
    def x(self):
        return self.location.point.x

    @property
    def y(self):
        return self.location.point.y


cart_map = {
    '>': EAST,
    '^': NORTH,
    '<': WEST,
    'v': SOUTH
}

reverse_cart_map = {
    EAST: '>',
    NORTH: '^',
    WEST: '<',
    SOUTH: 'v'
}


class Grid:

    def __init__(self, map, carts, width, height):
        self.map = map
        self.carts = carts
        self.width = width
        self.height = height

    def find_cart_order(self):
        return sorted(self.carts, key=lambda c: (c.y, c.x))

    def __repr__(self):
        world = ''
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                cart = next((c for c in self.carts if (c.x, c.y) == (x, y)), None)
                if cart is not None:
                    world += reverse_cart_map[cart.direction]
                elif (x, y) in self.map:
                    world += self.map[(x,y)].road
                else:
                    world += ' '
            world += '\n'
        return world


def build_map(data):
    map = {}
    carts = []
    max_width = 0
    max_height = 0
    for j, row in enumerate(data):
        for i, char in enumerate(row):
            point = Point(i,j)
            if char in '^v':
                road = '|'
            elif char in '<>':
                road = '-'
            elif char in '-|\\/+':
                road = char
            else:
                continue
            if char in '^v<>':
                carts.append(Cart(cart_map[char], Location(point, road, map)))
            map[(i, j)] = Location(point, road, map)
            if i > max_width:
                max_width = i
        if j > max_height:
            max_height = j
    return Grid(map, carts, max_width, max_height)


def solve(data):
    grid = build_map(data)
    collision = None
    while not collision:
        ordered_carts = grid.find_cart_order()
        for cart in ordered_carts:
            collision = cart.move()
            if collision:
                grid.remove(cart.location)
                print(collision)
                break
