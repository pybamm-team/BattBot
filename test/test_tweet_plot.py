import unittest
import pybamm
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tweet_plot import tweet_graph


class TestTweetPlot(unittest.TestCase):

    def setUp(self):
        self.sim = pybamm.Simulation(pybamm.lithium_ion.DFN())
        self.sim.solve([0, 3700])
        self.solution = self.sim.solution
        self.plot = pybamm.QuickPlot(solutions=self.solution, time_unit="seconds")
        self.plot.plot(1800)
        self.plot.fig.savefig("plot.png", dpi=300)

    def tearDown(self):
        assert not os.path.exists('plot.png')

    def test_tweet_graph(self):
        tweet_graph(testing=True)

if __name__ == '__main__':
    unittest.main()