import unittest
import pybamm
import os
from plotting.plot_graph import plot_graph


class TestPlotting(unittest.TestCase):

    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.parameter_values = self.model.default_parameter_values
        self.sim = pybamm.Simulation(self.model, parameter_values=self.parameter_values)

    def tearDown(self):
        os.remove('plot.png')

    def test_plot_graph_with_solution(self):
        self.sim.solve([0, 3700])
        solution = self.sim.solution
        plot_graph(solution=solution, sim=self.sim)
        path = 'plot.png'

        assert os.path.exists(path)

    def test_plot_graph_with_simulation(self):
        self.sim.solve([0, 3700])
        plot_graph(sim=self.sim)
        path = 'plot.png'

        assert os.path.exists(path)

if __name__ == '__main__':
    unittest.main()