import pybamm
import random
import numpy as np
import imageio
import os
import PIL
from PIL import Image, ImageSequence


def plot_graph(solution=None, sim=None):
    """
    This function generates and saves a plot.
    Parameters:
        solution: pybamm.Simulation.solution
            default: None
        sim: pybamm.Simulation
            default: None
    Returns:
        time: numerical (seconds)
    """

    # generating time to plot the simulation
    if solution is not None:
        t = solution["Time [s]"]
        final_time = int(t.entries[len(t.entries) - 1])
        time = random.randint(600, final_time)
        time_array = np.linspace(time - 600, time, num=25)
    else:
        time = random.randint(600, 3700)
        time_array = np.linspace(time - 600, time, num=25)

    images = []
    image_files = []
    for val in time_array:
        plot = pybamm.QuickPlot(sim, time_unit="seconds")
        plot.plot(val)
        images.append("plot" + str(val) + ".png")
        plot.fig.savefig("plot" + str(val) + ".png", dpi=150)

    for image in images:
        image_files.append(imageio.imread(image))
    imageio.mimsave('movie.gif', image_files, duration=0.1)

    for image in images:
        os.remove(image)

    size = 2048, 2048

    im = Image.open("movie.gif")

    frames = ImageSequence.Iterator(im)

    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.ANTIALIAS)
            yield thumbnail

    frames = thumbnails(frames)

    om = next(frames)
    om.info = im.info
    om.save("movie.gif", save_all=True, append_images=list(frames))

    return [time_array[0], time_array[-1]]


