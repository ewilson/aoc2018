def get_next_vals(n, m):
    return list(int(c) for c in str(n+m))


def cycle(x, scoreboard):
    return (x + 1 + scoreboard[x]) % len(scoreboard)


def solve(steps):
    scoreboard = [3, 7]
    a, b = 0, 1
    while len(scoreboard) - 10 < steps:
        scoreboard.extend(get_next_vals(scoreboard[a], scoreboard[b]))
        a = cycle(a, scoreboard)
        b = cycle(b, scoreboard)
    return ''.join(str(n) for n in scoreboard[steps:steps+10])


def exact_match(nums, tail):
    return nums == tail[-len(nums):]


def found(nums, tail):
    if len(tail) < len(nums):
        return False
    else:
        return exact_match(nums, tail) or nums == tail[-len(nums)-1:-1]


def solve2(input):
    scoreboard = [3, 7]
    a, b = 0, 1
    input_nums = [int(s) for s in input]
    while not found(input_nums, scoreboard[-(len(input)+1):]):
        scoreboard.extend(get_next_vals(scoreboard[a], scoreboard[b]))
        a = cycle(a, scoreboard)
        b = cycle(b, scoreboard)
    return len(scoreboard) - len(input) if exact_match(input_nums, scoreboard) else len(scoreboard) - len(input) - 1
