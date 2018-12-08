from common import readfile


class Node:

    def __init__(self, header):
        self.header = header
        self.children = []
        self.metadata = []

    def needs_children(self):
        return len(self.children) < self.header[0]

    def needs_metadata(self):
        return len(self.metadata) < self.header[1]

    def complete(self):
        return not self.needs_children() and not self.needs_metadata()

    def sum_metadata(self):
        return sum(self.metadata) + sum([c.sum_metadata() for c in self.children])

    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum([self.children[m - 1].value() for m in self.metadata if 0 < m <= len(self.children)])

    def __repr__(self):
        return f'<[{self.header[0]}, {self.header[1]}], C:{self.children}, M:{self.metadata}'


def solve(data):
    stack = []
    while data:
        if not stack or stack[-1].needs_children():
            stack.append(Node((data.pop(0), data.pop(0))))
        elif stack[-1].needs_metadata():
            stack[-1].metadata.append(data.pop(0))
        elif stack[-1].complete():
            if len(stack) == 1:
                break
            else:
                top = stack.pop()
                stack[-1].children.append(top)
    return stack[0].value()


def transformer(line):
    return [int(n) for n in line.strip().split()]


def get_test_data():
    return readfile('d08/test.txt', transformer)[0]


def get_real_data():
    return readfile('d08/data.txt', transformer)[0]
