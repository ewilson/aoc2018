def addr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] + regs[b]
    return cp_regs


def addi(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] + b
    return cp_regs


def mulr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] * regs[b]
    return cp_regs


def muli(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] * b
    return cp_regs


def banr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] & regs[b]
    return cp_regs


def bani(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] & b
    return cp_regs


def borr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] | regs[b]
    return cp_regs


def bori(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a] | b
    return cp_regs


def setr(regs, a, _, c):
    cp_regs = list(regs)
    cp_regs[c] = regs[a]
    return cp_regs


def seti(regs, a, _, c):
    cp_regs = list(regs)
    cp_regs[c] = a
    return cp_regs


def gtir(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if a > regs[b] else 0
    return cp_regs


def gtri(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if regs[a] > b else 0
    return cp_regs


def gtrr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if regs[a] > regs[b] else 0
    return cp_regs


def eqir(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if a == regs[b] else 0
    return cp_regs


def eqri(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if regs[a] == b else 0
    return cp_regs


def eqrr(regs, a, b, c):
    cp_regs = list(regs)
    cp_regs[c] = 1 if regs[a] == regs[b] else 0
    return cp_regs

lookup = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}
