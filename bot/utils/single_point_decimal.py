import random


def single_decimal_point(start, stop, step):
    """
    Generates a random number with only one decimal
    digit.
    Parameters:
        start: numerical
        stop: numerical
        step: numerical
    Returns:
        rand_num: numerical
    """
    start = start
    stop = stop
    step = step
    precision = 0.1
    f = 1 / precision
    rand_num = random.randrange(start * f, stop * f, step * f) / f
    return rand_num
