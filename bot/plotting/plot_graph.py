import pybamm
import random
import numpy as np
import imageio
import os
from PIL import Image, ImageSequence
from utils.resize_gif import resize_gif
import matplotlib.pyplot as plt


def plot_graph(solution=None, sim=None):
    """
    This function generates 30 plots over a time
    span of 800 seconds and then compiles them to
    create a GIF.
    Parameters:
        solution: pybamm.Simulation.solution
            default: None
        sim: pybamm.Simulation
            default: None
    Returns:
        time: list
    """

    # generating time to plot the simulation
    if solution is not None:
        t = solution["Time [s]"]
        final_time = int(t.entries[len(t.entries) - 1])
        time = random.randint(800, final_time)
        time_array = np.linspace(time - 800, time, num=25)
    else:
        time = random.randint(800, 3700)
        time_array = np.linspace(time - 800, time, num=25)

    images = []
    image_files = []

    for val in time_array:
        plot = pybamm.QuickPlot(sim, time_unit="seconds")
        plot.plot(val)
        images.append("plot" + str(val) + ".png")
        plot.fig.savefig("plot" + str(val) + ".png", dpi=200)
        plt.close()

    for image in images:
        image_files.append(imageio.imread(image))
    imageio.mimsave('plot.gif', image_files, duration=0.1)

    for image in images:
        os.remove(image)

    orig_gif = Image.open("plot.gif")
    frames = ImageSequence.Iterator(orig_gif)
    frames = resize_gif(frames)

    new_gif = next(frames)
    new_gif.info = orig_gif.info
    new_gif.save("plot.gif", save_all=True, append_images=list(frames))
    orig_gif.close()

    return [time_array[0], time_array[-1]]
