import pybamm
import random
from utils.single_point_decimal import single_decimal_point
from plotting.plot_graph import plot_graph

def experiment_generator():
    charge = []
    discharge = []
    rest = []
    hold = []

    vmin = single_decimal_point(3.2, 3.7, 0.1)
    vmax = single_decimal_point(3.7, 4.2, 0.1)
    ccharge = random.randint(1, 5)
    cdischarge = random.randint(1, 5)
    ccutoff = random.randint(1, 100)
    # if vmin < vmax:
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
    if random.randint(0, 1) == 0:
        cycle.append(rest[0][0])
    cycle.append(charge[0])
    cycle.append(hold[0])
    if random.randint(0, 1) == 0:
        cycle.append(rest[0][1])

    number = random.randint(1, 3)
    print(cycle * number)
    return cycle, number

