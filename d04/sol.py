from common import readfile


TEST_DATA = True


def solve():
    filename = 'test.txt' if TEST_DATA else 'data.txt'
    
    data = readfile(filename)
