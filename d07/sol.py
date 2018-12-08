from string import ascii_uppercase
from collections import defaultdict

from common import readfile


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


def solve(data):
    graph = build_graph(data)
    steps = []
    while graph:
        for letter in ascii_uppercase:
            if letter in graph and not graph[letter]:
                steps.append(letter)
                purge_step(graph, letter)
                break
    return ''.join(steps)


class Worker:

    def __init__(self):
        self.available = True
        self.time_remaining = 0
        self.step = None

    def accept_job(self, step, time):
        self.time_remaining = time
        self.step = step
        self.available = False

    def go(self, time):
        self.time_remaining -= time

    def release_job(self):
        self.available = True
        done_step = self.step
        self.step = None
        return done_step

    def __repr__(self):
        return f'{self.available} -- {self.time_remaining} -- {self.step}'


class Team:

    def __init__(self, number):
        self.workers = [Worker() for _ in range(number)]

    def find_available_workers(self):
        return [w for w in self.workers if w.available]

    def time_next_complete(self):
        return min([w.time_remaining for w in self.workers if w.time_remaining > 0], default=0)

    def go(self, time):
        [w.go(time) for w in self.workers if not w.available]
        return [w.release_job() for w in self.workers if w.time_remaining == 0 and not w.available]

    def find_active_jobs(self):
        return {w.step for w in self.workers}


def get_ready_jobs(graph, n, active_jobs):
    steps = []
    for letter in ascii_uppercase:
        if letter in graph and not graph[letter] and letter not in active_jobs:
            steps.append(letter)
        if len(steps) >= n:
            break
    return steps


def assign_jobs(available_workers, jobs, minimum_step_time):
    for w in available_workers:
        if jobs:
            letter = jobs.pop()
            w.accept_job(letter, minimum_step_time + ascii_uppercase.index(letter) + 1)


def solve2(data, num_workers=5, minimum_step_time=60):
    graph = build_graph(data)
    time = 0
    team = Team(num_workers)
    while graph:
        available_workers = team.find_available_workers()
        jobs = [j for j in get_ready_jobs(graph, len(available_workers), team.find_active_jobs())]
        assign_jobs(available_workers, jobs, minimum_step_time)
        time_increment = team.time_next_complete()
        time += time_increment
        complete_jobs = team.go(time_increment)
        for job in complete_jobs:
            purge_step(graph, job)
    return time


def transformer(line):
    split_line = line.split()
    return split_line[1], split_line[7]


def get_test_data():
    return readfile('d07/test.txt', transformer)


def get_real_data():
    return readfile('d07/data.txt', transformer)
