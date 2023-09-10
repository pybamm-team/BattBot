import random
from utils.desired_decimal_point_generator import desired_decimal_point_generator
import logging


def experiment_generator(testing={"rest1": False, "rest2": False}):
    """
    This function generates a random experiment with the template
    ["Discharge", "Rest?", "Charge", "Hold", "Rest?"].

    Parameters
    ----------

        testing : dict
            default : {"rest1": False, "rest2": False}
            This should only be used while testing, to generate some
            not so random experiments.

    Returns
    -------
        cycle : list
    """
    charge = []
    discharge = []
    rest = []
    hold = []

    vmin = desired_decimal_point_generator(3.2, 3.7, 1)
    vmax = desired_decimal_point_generator(3.7, 4.2, 1)
    ccharge = random.randint(1, 2)
    cdischarge = random.randint(1, 2)
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

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(str([tuple(cycle)]))

    return [tuple(cycle)]
