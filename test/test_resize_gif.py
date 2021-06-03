import unittest
import pybamm
import os
from bot.utils.resize_gif import resize_gif
import numpy as np
import random
import imageio
from PIL import Image, ImageSequence


class TestResizeGif(unittest.TestCase):

    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.parameter_values = self.model.default_parameter_values
        self.sim = pybamm.Simulation(
            self.model,
            parameter_values=self.parameter_values
        )
        self.sim.solve([0, 3700])
        self.solution = self.sim.solution

        self.t = self.solution["Time [s]"]
        self.final_time = int(self.t.entries[len(self.t.entries) - 1])
        self.time = random.randint(800, self.final_time)
        self.time_array = np.linspace(self.time - 800, self.time, num=25)

        self.images = []
        self.image_files = []
        for val in self.time_array:
            self.plot = pybamm.QuickPlot(self.sim, time_unit="seconds")
            self.plot.plot(val)
            self.images.append("plot" + str(val) + ".png")
            self.plot.fig.savefig("plot" + str(val) + ".png", dpi=200)

        for image in self.images:
            self.image_files.append(imageio.imread(image))
        imageio.mimsave('plot.gif', self.image_files, duration=0.1)

        for image in self.images:
            os.remove(image)

    def tearDown(self):
        os.remove("plot.gif")

    def test_resize_gif(self):
        orig_gif = Image.open("plot.gif")
        frames = ImageSequence.Iterator(orig_gif)
        frames = resize_gif(frames)

        new_gif = next(frames)
        new_gif.info = orig_gif.info
        new_gif.save("plot.gif", save_all=True, append_images=list(frames))
        orig_gif.close()

        self.assertTrue(os.path.exists("plot.gif"))

        gif = Image.open("plot.gif")
        width, height = gif.size
        gif.close()

        self.assertTrue(width == 1440)
        self.assertTrue(height <= 1440)
        self.assertTrue(os.stat("plot.gif").st_size <= 5000000)


if __name__ == "__main__":
    unittest.main()
