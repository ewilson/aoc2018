def readfile(filename, transformer=lambda x: x):
    f = open(filename)
    return [transformer(s.strip()) for s in f.readlines()]

