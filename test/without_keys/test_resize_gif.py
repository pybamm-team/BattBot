import unittest
import pybamm
import os
from bot.utils.resize_gif import resize_gif
import numpy as np
import imageio
from PIL import Image
import matplotlib.pyplot as plt
import gc


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
        self.time_array = np.linspace(0, self.final_time, num=3)

        self.images = []
        self.image_files = []
        for val in self.time_array:
            self.plot = pybamm.QuickPlot(self.sim, time_unit="seconds")
            self.plot.plot(val)
            self.images.append("plot" + str(val) + ".png")
            self.plot.fig.savefig("plot" + str(val) + ".png", dpi=200)
            plt.close()

        for image in self.images:
            self.image_files.append(imageio.imread(image))
        imageio.mimsave('plot.gif', self.image_files, duration=0.1)

        for image in self.images:
            os.remove(image)

    def tearDown(self):
        os.remove("plot.gif")

    def test_resize_gif(self):
        resize_gif("plot.gif", (1440, 1440))

        self.assertTrue(os.path.exists("plot.gif"))

        gif = Image.open("plot.gif")
        width, height = gif.size
        gif.close()

        del gif
        gc.collect()

        self.assertTrue(width == 1440)
        self.assertTrue(height <= 1440)
        self.assertTrue(os.stat("plot.gif").st_size <= 15000000)


if __name__ == "__main__":
    unittest.main()
