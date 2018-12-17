import d16.ops as ops


class Sample:

    def __init__(self, before, instruction, after):
        self.before = before
        self.opcode = instruction[0]
        self.instruction = instruction[1:]
        self.after = after


s = Sample([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1])


for op in ops.lookup:
    result = ops.lookup[op](s.before, *s.instruction)
    if result == s.after:
        print(f"SUCCESS: {op} give {result}")
    else:
        print(f'nope: {op} gives {result}')


def read_input():
    f = open('d16/data.txt')
    lines = [line.strip() for line in f.readlines()]
    samples = []

