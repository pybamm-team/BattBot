import random


def single_decimal_point(start, stop, step):
    start = start
    stop = stop
    step = step
    precision = 0.1
    f = 1 / precision
    return random.randrange(start * f, stop * f, step * f) / f
