import pybamm
import numpy as np
import matplotlib.pyplot as plt


# Reference - PyBaMM example notebook -
# https://github.com/pybamm-team/PyBaMM/blob/develop/examples/notebooks/simulating-long-experiments.ipynb
def generate_summary_variables(solutions, chemistry):
    """
    Plots summary variables.
    Parameters:
        solutions: list
        chemistry: dict
    """

    if chemistry == pybamm.parameter_sets.Ai2020:
        vars_to_plot = [
            "Measured capacity [A.h]",
            "Loss of lithium inventory [%]",
            "Loss of active material in negative electrode [%]",
            "Loss of active material in positive electrode [%]",
        ]
    else:
        vars_to_plot = [
            "Capacity [A.h]",
            "Loss of lithium inventory [%]",
            "Loss of active material in negative electrode [%]",
            "Loss of active material in positive electrode [%]",
            "x_100",
            "x_0",
            "y_100",
            "y_0",
        ]

    length = len(vars_to_plot)
    n = int(length // np.sqrt(length))
    m = int(np.ceil(length / n))

    # fig = plt.figure(figsize=(15, 8))
    fig, axes = plt.subplots(n, m, figsize=(15, 8))
    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
    for var, ax in zip(vars_to_plot, axes.flat):
        for solution in solutions:
            ax.plot(
                solution.summary_variables["Cycle number"],
                solution.summary_variables[var],
                # label = 'x'
            )
        ax.set_xlabel("Cycle number")
        ax.set_ylabel(var)
        ax.set_xlim([1, solution.summary_variables["Cycle number"][-1]])

    plt.subplots_adjust(top=0.00001)
    fig.tight_layout()
    fig.legend(['This is plot 1', 'This is plot 2'],loc='lower right', bbox_to_anchor=(1,0), bbox_transform=plt.gcf().transFigure)
    plt.savefig("plot.png", dpi=300)
