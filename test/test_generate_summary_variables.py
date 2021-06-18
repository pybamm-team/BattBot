import unittest
import pybamm
import os
from bot.plotting.summary_variables import generate_summary_variables


class TestPlottingSummaryVariables(unittest.TestCase):
    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.experiment = pybamm.Experiment(
            [
                (
                    "Discharge at C/10 for 10 hours or until 3.3 V",
                    "Rest for 1 hour",
                    "Charge at 1 A until 4.1 V",
                    "Hold at 4.1 V until 50 mA",
                    "Rest for 1 hour"
                )
            ]
            * 10,
            termination="80% capacity"
        )
        self.sim = pybamm.Simulation(
            self.model,
            experiment=self.experiment,
            solver=pybamm.CasadiSolver()
        )
        self.sim.solve()
        self.solution = self.sim.solution

    def tearDown(self):
        os.remove("plot.png")

    def test_generate_summary_variables(self):
        generate_summary_variables(solutions=[self.solution])
        path = "plot.png"

        assert os.path.exists(path)


if __name__ == "__main__":
    unittest.main()
