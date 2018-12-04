from common import readfile

from datetime import datetime
from collections import namedtuple
from collections import defaultdict


TEST_DATA = True

Entry = namedtuple('Entry', 'timestamp,event')

class Shift:
    def __init__(self, guard_id, starttime):
        self.guard_id = guard_id
        self.timestamp = starttime
        self.events = []

    def __repr__(self):
        return f'Guard #{self.guard_id} -- {self.timestamp.day}'

 
Event = namedtuple('Event', 'timestamp,wake')

def transformer(line):
    timestamp = datetime.strptime(line[1:17], '%Y-%m-%d %H:%M')
    event = line[19:]
    return Entry(timestamp, event)


def into_shifts(entries):
    shifts = []
    shift = None
    for e in entries:
        event = e.event
        if event[0:5] == 'Guard':
            if shift is not None:
                shifts.append(shift)
            shift = Shift(event.split()[1][1:], e.timestamp)
            shift.events.append(Event(e.timestamp, True))
        elif event == 'falls asleep':
            shift.events.append(Event(e.timestamp, False))
        elif event == 'wakes up':
            shift.events.append(Event(e.timestamp, True))
    shifts.append(shift)
    return shifts


def shift_summary(shift):
    minute = 0
    summary = []
    awake = True
    for event in shift.events:
        if event.timestamp.hour == 23:
            continue
        while minute < event.timestamp.minute:
            summary.append(awake)
            minute += 1
        awake = event.wake
    for m in range(minute, 60):
        summary.append(awake)
    return summary


def solve(test_data=TEST_DATA):
    filename = 'test.txt' if test_data else 'data.txt'
    
    data = readfile(filename, transformer)
    sorted_data = sorted(data, key=lambda e: e.timestamp)
    
    shifts = into_shifts(sorted_data)
    totals = defaultdict(int)
    for s in shifts:
        totals[s.guard_id] += sum([not w for w in shift_summary(s)])
    sleepy = max(totals, key=totals.get)
    sleepy_shifts = [s for s in shifts if s.guard_id == sleepy]
    offenses = [0] * 60
    for m in range(60):
        for s in sleepy_shifts:
            ss = shift_summary(s)
            offenses[m] += 1 if not ss[m] else 0

    guard_history = defaultdict(list)
    for s in shifts:
        guard_history[s.guard_id].append(shift_summary(s))
    
    guard, minute, total = '', 0, 0
    for g in guard_history:
        summary = [0] * 60
        for s in guard_history[g]:
            for m in range(60):
                summary[m] += 1 if not s[m] else 0
        best_val = max(summary)
        if best_val > total:
            guard = g
            minute = summary.index(best_val)
            total = best_val
            
    print(guard, minute, total)
            
    return int(guard) * minute
