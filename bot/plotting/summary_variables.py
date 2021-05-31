import numpy as np
import matplotlib.pyplot as plt


def generate_summary_variables(solution):
    """
    Plots summary variables.
    Parameters:
        solution: pybamm.Simulation.solution
    """

    vars_to_plot = [
        "Capacity [A.h]",
        "Loss of lithium inventory [%]",
        "Loss of capacity to negative electrode SEI [A.h]",
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

    fig, axes = plt.subplots(n, m, figsize=(10, 10))
    for var, ax in zip(vars_to_plot, axes.flat):
        ax.plot(
            solution.summary_variables["Cycle number"],
            solution.summary_variables[var]
        )
        ax.set_xlabel("Cycle number")
        ax.set_ylabel(var)
        ax.set_xlim([1, solution.summary_variables["Cycle number"][-1]])
    fig.tight_layout()
    plt.savefig("plot.png", dpi=300)
