from common import readfile


class Node:

    def __init(self, header, children, metadata):
        self.header = header
        self.children = children
        self.metadata = metadata


def transformer(line):
    return [int(n) for n in line.strip().split()]


def get_test_data():
    return readfile('d08/test.txt', transformer)[0]


def get_real_data():
    return readfile('d08/data.txt', transformer)[0]
