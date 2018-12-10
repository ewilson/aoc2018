from collections import defaultdict


class DoubleLinkedList:

    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def append(self, dll):
        self.next = dll
        dll.prev = self

    def insert_value_after(self, val):
        new_node = DoubleLinkedList(val)
        if self.next is not None:
            self.next.prev = new_node
        new_node.next = self.next

        self.next = new_node
        new_node.prev = self
        return new_node

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.val

    def insert_value_after_next(self, val):
        return self.next.insert_value_after(val)

    def __repr__(self):
        return f'<{self.val}>'


class Circle(DoubleLinkedList):

    def __init__(self, val):
        super().__init__(val)
        self.next = self
        self.prev = self


def solve(num_players, max_num):
    current = Circle(0)
    score = defaultdict(int)
    for n in range(1, max_num + 1):
        if n % 23 == 0:
            score[n % num_players] += n
            current = current.prev.prev.prev.prev.prev.prev
            score[n % num_players] += current.prev.remove()
        else:
            current = current.insert_value_after_next(n)
    print(max(score.values()))
    return current
