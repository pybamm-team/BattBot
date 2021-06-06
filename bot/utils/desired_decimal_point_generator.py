import random


def desired_decimal_point_generator(start, stop, step):
    """
    Generates a random number with desired number
    of decimal digits.
    Parameters:
        start: numerical
        stop: numerical
        step: numerical
    Returns:
        rand_num: numerical
    """
    rand_num = round(random.uniform(start, stop), step)
    return rand_num
