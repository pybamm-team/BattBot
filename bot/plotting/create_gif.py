import pybamm
import numpy as np
import imageio
import os
from utils.resize_gif import resize_gif
import matplotlib.pyplot as plt


def create_gif(batch_study, labels=None):
    """
    This function generates 80 plots over a time
    span of t_eval seconds and then compiles them to
    create a GIF.
    Parameters:
        batch_study: pybamm.BatchStudy
        labels: list
            default: None
            A list of labels for the GIF.
    """

    # generating time to plot the simulation
    max_time = 0
    solution = batch_study.sims[0].solution
    for sim in batch_study.sims:
        if sim.solution["Time [s]"].entries[-1] > max_time:
            max_time = sim.solution["Time [s]"].entries[-1]
            solution = sim.solution

    t = solution["Time [s]"]
    final_time = int(t.entries[len(t.entries) - 1])
    time_array = np.linspace(int(t.entries[0]), final_time, num=80)

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

    # creating 80 comparison plots
    for val in time_array:
        plot = pybamm.QuickPlot(
            batch_study.sims,
            time_unit="seconds",
            labels=labels,
            output_variables=output_variables,
        )
        plot.plot(val)
        images.append("plot" + str(val) + ".png")
        plot.fig.savefig("plot" + str(val) + ".png", dpi=300)
        plt.close()

    print("PLOTS CREATED")

    # compiling the plots to create a GIF
    with imageio.get_writer('plot1.gif', mode='I', duration=0.1) as writer:
        for image in images:
            writer.append_data(imageio.imread(image))


    print("GIF CREATED")

    for image in images:
        os.remove(image)

    # resizing the GIF for Twitter
    resize_gif("plot.gif", resize_to=(1440, 1440))
