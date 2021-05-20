import unittest
import pybamm
import os
import importlib.util
import pytest
from plotting.plot_graph import plot_graph


class TestPlotting(unittest.TestCase):

    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.parameter_values = self.model.default_parameter_values

    def tearDown(self):
        os.remove('plot.png')

    def test_plot_graph(self):
        sim = pybamm.Simulation(self.model, parameter_values=self.parameter_values)
        sim.solve([0, 3600])
        solution = sim.solution
        plot_graph(solution=solution, sim=sim)
        path = 'plot.png'

        assert os.path.exists(path)

if __name__ == '__main__':
    unittest.main()