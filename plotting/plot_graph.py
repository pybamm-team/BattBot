import pybamm
import random


def plot_graph(solution=None, sim=None):
    """
    This function generates and saves a plot.
    Parameters:
        solution: pybamm.Simulation.solution
        sim: pybamm.Simulation
    Returns:
        time: numerical (seconds)
    """

    # generating time to plot the simulation
    if solution is not None:
        t = solution["Time [s]"]
        final_time = int(t.entries[len(t.entries) - 1])
        time = random.randint(0, final_time)
    else:
        time =random.randint(0, 3700)

    # generating a plot
    plot = pybamm.QuickPlot(sim, time_unit="seconds")
    plot.plot(time)

    # saving the plot
    plot.fig.savefig("plot.png", dpi=300)

    return time