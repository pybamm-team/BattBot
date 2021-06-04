import random
from utils.single_point_decimal import single_decimal_point


def experiment_generator(testing={"rest1": False, "rest2": False}):
    """
    This function generates a random experiment with the template
    ["Discharge", "Rest?", "Charge", "Hold", "Rest?"].
    Parameters:
        testing: dict
            default: {"rest1": False, "rest2": False}
        keys: rest1, rest2
    Returns:
        cycle: list
        number: numerical
    """
    charge = []
    discharge = []
    rest = []
    hold = []

    vmin = single_decimal_point(3.2, 3.7, 0.1)
    vmax = single_decimal_point(3.7, 4.2, 0.1)
    ccharge = random.randint(1, 3)
    cdischarge = random.randint(1, 3)
    ccutoff = random.randint(1, 100)

    discharge.append(
        "Discharge at " + str(cdischarge) + " C until " + str(vmin) + " V",
    )

    charge.append(
        "Charge at " + str(ccharge) + " C until " + str(vmax) + " V",
    )

    rest.append(
        [
            "Rest for " + str(random.randint(1, 10)) + " minutes",
            "Rest for " + str(random.randint(1, 10)) + " minutes",
        ]
    )

    hold.append(
        "Hold at " + str(vmax) + " V until " + str(ccutoff) + " mA",
    )

    random.shuffle(rest)

    cycle = []

    cycle.append(discharge[0])
    if random.randint(0, 1) == 1 or testing["rest1"]:
        cycle.append(rest[0][0])
    cycle.append(charge[0])
    cycle.append(hold[0])
    if random.randint(0, 1) == 1 or testing["rest2"]:
        cycle.append(rest[0][1])

    number = random.randint(1, 50)
    # print(cycle, number)
    return [tuple(cycle)], number
