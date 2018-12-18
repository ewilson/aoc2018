import re

from common import readfile

import d16.ops as ops


class Sample:

    def __init__(self, before, instruction, after):
        self.before = before
        self.opcode = instruction[0]
        self.instruction = instruction[1:]
        self.after = after
        self.possible_ops = []

    def __repr__(self):
        return f'\nBefore: {self.before}\n{self.opcode} {self.instruction}\nAfter: {self.after}\n'


class Instruction:

    def __init__(self, op, input_a, input_b, output):
        self.op = op
        self.input_a = input_a
        self.input_b = input_b
        self.output = output

    def apply(self, register):
        return self.op(register, self.input_a, self.input_b, self.output)

    def __repr__(self):
        return f'{self.op} {self.input_a} {self.input_b} {self.output}'


def read_input():
    f = open('d16/data.txt')
    lines = [line.strip() for line in f.readlines()]
    line_iter = iter(lines)
    samples = []
    while True:
        try:
            first_line = next(line_iter)
            before_match = re.match('Before:\s+(\[\d+, \d+, \d+, \d+\])', first_line)
            if before_match is None:
                print(f'NOT MATCH (1) {first_line}')
                break
            before_list = eval(before_match.group(1))
            instruction_line = next(line_iter)
            instructions = [int(s) for s in instruction_line.split()]
            after_line = next(line_iter)
            after_match = re.match('After:\s+(\[\d+, \d+, \d+, \d+\])', after_line)
            if after_match is None:
                print(f'NOT MATCH (3) {after_line}')
                break
            after_list = eval(after_match.group(1))
            samples.append(Sample(before_list, instructions, after_list))
            _ = next(line_iter)
        except StopIteration:
            break
    return samples


def transformer(line):
    return [int(n) for n in line.strip().split()]


def read_input2(functions):
    input = readfile('d16/data2.txt', transformer)
    return [Instruction(functions[i[0]], *i[1:]) for i in input]


def find_possible_ops(s):
    for op in ops.lookup:
        result = ops.lookup[op](s.before, *s.instruction)
        if result == s.after:
            s.possible_ops.append(op)


def find_op(n, samples):
    sets = [set(s.possible_ops) for s in samples if s.opcode == n]
    return set.intersection(*sets)


def purge(solved, n, answers):
    for i in range(16):
        if i != n:
            answers[i] -= {solved}


def translate(answers):
    functions = {}
    for n in answers:
        name, = answers[n]
        functions[n] = ops.lookup[name]
    return functions


def solve():
    samples = read_input()
    [find_possible_ops(s) for s in samples]
    answers = {}
    for n in range(16):
        answers[n] = find_op(n, samples)
    not_done = True
    while not_done:
        for n in range(16):
            if len(answers[n]) == 1:
                (solved, ) = answers[n]
                purge(solved, n, answers)
        not_done = False
        for n in answers:
            if len(answers[n]) > 1:
                not_done = True
                break
    functions = translate(answers)
    instructions = read_input2(functions)
    reg = [0, 0, 0, 0]
    for inst in instructions:
        reg = inst.apply(reg)
        print(reg)
    return reg
