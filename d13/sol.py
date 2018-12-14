from common import readfile


def get_test_data():
    return readfile('d13/test.txt', transformer=list)


def get_real_data():
    return readfile('d13/data.txt', transformer=list)
