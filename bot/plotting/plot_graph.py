import pybamm
import numpy as np
import imageio
import os
from utils.resize_gif import resize_gif
import matplotlib.pyplot as plt


def plot_graph(solution=None, sim=None, labels=None):
    """
    This function generates 80 plots over a time
    span of t_eval seconds and then compiles them to
    create a GIF.
    Parameters:
        solution: pybamm.Simulation.solution or list
            default: None
        sim: pybamm.Simulation
            default: None
        labels: list
            default: None
            A list of labels for the GIF.
    """

    # generating time to plot the simulation
    if solution is not None:
        t = solution["Time [s]"]
        final_time = int(t.entries[len(t.entries) - 1])
        time_array = np.linspace(int(t.entries[0]), final_time, num=80)
    else:
        time_array = np.linspace(0, 3700, num=80)

    images = []
    image_files = []

    output_variables = [
        "Negative particle surface concentration [mol.m-3]",
        "Electrolyte concentration [mol.m-3]",
        "Positive particle surface concentration [mol.m-3]",
        "Current [A]",
        "Negative electrode potential [V]",
        "Electrolyte potential [V]",
        "Positive electrode potential [V]",
        "Terminal voltage [V]",
    ]

    for val in time_array:
        plot = pybamm.QuickPlot(
            sim,
            time_unit="seconds",
            labels=labels,
            output_variables=output_variables,
        )
        plot.plot(val)
        images.append("plot" + str(val) + ".png")
        plot.fig.savefig("plot" + str(val) + ".png", dpi=300)
        plt.close()

    for image in images:
        image_files.append(imageio.imread(image))
    imageio.mimsave('plot.gif', image_files, duration=0.1)

    for image in images:
        os.remove(image)

    resize_gif("plot.gif", resize_to=(1440, 1440))
