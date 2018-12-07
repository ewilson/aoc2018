from string import ascii_uppercase
from collections import defaultdict

from common import readfile


def transformer(line):
    split_line = line.split()
    return split_line[1], split_line[7]


def build_graph(data):
    prereqs = defaultdict(set)
    for start, end in data:
        prereqs[end].add(start)
        if start not in prereqs:
            prereqs[start] = set()
    return prereqs


def purge_step(graph, letter):
    for element in graph:
        graph[element].discard(letter)
    del graph[letter]


def solve(real):
    filename = 'd07/data.txt' if real else 'd07/test.txt'
    data = readfile(filename, transformer)
    graph = build_graph(data)
    steps = []
    while graph:
        for letter in ascii_uppercase:
            if letter in graph and not graph[letter]:
                steps.append(letter)
                purge_step(graph, letter)
                break
    return ''.join(steps)


def test():
    return solve(False)


def answer():
    return solve(True)
