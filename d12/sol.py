initial_state = '.##..##..####..#.#.#.###....#...#..#.#.#..#...#....##.#.#.#.#.#..######.##....##.###....##..#.####.#'
test_initial_state = '#..#.#..##......###...###'

test_rules = {
    "...##": "#",
    "..#..": "#",
    ".#...": "#",
    ".#.#.": "#",
    ".#.##": "#",
    ".##..": "#",
    ".####": "#",
    "#.#.#": "#",
    "#.###": "#",
    "##.#.": "#",
    "##.##": "#",
    "###..": "#",
    "###.#": "#",
    "####.": "#"
}

rules = {
    ".#...": "#",
    "#....": ".",
    "#.###": ".",
    "#.##.": ".",
    "#...#": ".",
    "...#.": ".",
    ".#..#": "#",
    ".####": "#",
    ".###.": ".",
    "###..": "#",
    "#####": ".",
    "....#": ".",
    ".#.##": "#",
    "####.": ".",
    "##.#.": "#",
    "#.#.#": "#",
    "..#.#": ".",
    ".#.#.": "#",
    "###.#": "#",
    "##.##": ".",
    "..#..": ".",
    ".....": ".",
    "..###": "#",
    "#..##": "#",
    "##...": "#",
    "...##": "#",
    "##..#": ".",
    ".##..": "#",
    "#..#.": ".",
    "#.#..": "#",
    ".##.#": ".",
    "..##.": ".",
}


def result(neighborhood, rules):
    key = ''.join(neighborhood)
    if key in rules:
        plant = rules[key]
    else:
        plant = '.'
    return plant


class World:

    def __init__(self, pos, neg, rules):
        self.pos = pos
        if neg is None:
            self.neg = ['.'] * 5
            self.neg[0] = self.pos[0]
        else:
            self.neg = neg
        self.rules = rules

    @staticmethod
    def _extend(row):
        last_five = row[-5:]
        extend_by = 0 if '#' not in last_five else ''.join(last_five).rindex('#')
        row.extend(['.'] * extend_by)

    def extend_rows(self):
        self._extend(self.pos)
        self._extend(self.neg)

    def _find_next(self, row):
        next_state = ['.'] * len(row)
        for i, _ in enumerate(row):
            if i < 2 or len(row) - i <= 2:
                continue
            next_state[i] = result(row[i - 2: i + 3], self.rules)
        return next_state

    def iterate(self):
        self.extend_rows()
        next_pos = self._find_next(self.pos)
        next_neg = self._find_next(self.neg[::-1])[::-1]
        next_middle = self._find_next(self.neg[3:0:-1] + self.pos[:4])
        next_pos[0] = next_middle[3]
        next_pos[1] = next_middle[4]
        next_neg[0] = next_middle[3]
        next_neg[1] = next_middle[2]
        return World(next_pos, next_neg, self.rules)

    def sum(self):
        total = 0
        for i, plant in enumerate(self.pos):
            if plant == '#':
                total += i
        for i, plant in enumerate(self.neg):
            if plant == '#':
                total -= i
        return total

    def __repr__(self):
        return ' ' * (len(self.neg)-1) + '0' + 9*' ' + '0' + 9*' ' + '0\n' + ''.join(self.neg[:0:-1] + self.pos)


def solve(current, rules, num=20):
    w = World(list(current), None, rules)
    max_neg = 0
    for generation in range(num):
        max_neg = len(w.neg) if len(w.neg) > max_neg else max_neg
        w = w.iterate()
    print('-', max_neg)
    return w

