import unittest
import pybamm
import os
from bot.plotting.plot_graph import plot_graph


class TestPlotting(unittest.TestCase):
    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.parameter_values = self.model.default_parameter_values
        self.sim = pybamm.Simulation(
            self.model,
            parameter_values=self.parameter_values
        )

    def tearDown(self):
        os.remove("plot.gif")

    def test_plot_graph_with_solution(self):
        self.sim.solve([0, 3700])
        solution = self.sim.solution
        time_array = plot_graph(solution=solution, sim=self.sim)
        path = "plot.gif"

        self.assertIsInstance(time_array, list)
        self.assertTrue(len(time_array) == 2)
        assert os.path.exists(path)

    def test_plot_graph_with_simulation(self):
        self.sim.solve([0, 3700])
        time_array = plot_graph(sim=self.sim)
        path = "plot.gif"

        self.assertIsInstance(time_array, list)
        self.assertEqual(len(time_array), 2)
        self.assertLessEqual(time_array[-1], 3700)
        self.assertGreaterEqual(time_array[0], 0)
        assert os.path.exists(path)


if __name__ == "__main__":
    unittest.main()
