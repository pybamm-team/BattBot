import unittest
import pybamm
import os
from bot.plotting.summary_variables import generate_summary_variables


class TestPlottingSummaryVariables(unittest.TestCase):
    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.chemistry_Ai2020 = pybamm.parameter_sets.Ai2020
        self.chemistry_Chen2020 = pybamm.parameter_sets.Chen2020
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
        )
        self.sim_Chen = pybamm.Simulation(
            self.model,
            experiment=self.experiment,
            parameter_values=pybamm.ParameterValues(
                chemistry=self.chemistry_Chen2020
            ),
            solver=pybamm.CasadiSolver()
        )
        self.sim_Chen.solve()
        self.solution_Chen = self.sim_Chen.solution
        self.sim_Ai = pybamm.Simulation(
            self.model,
            experiment=self.experiment,
            parameter_values=pybamm.ParameterValues(
                chemistry=self.chemistry_Ai2020
            ),
            solver=pybamm.CasadiSolver()
        )
        self.sim_Ai.solve(calc_esoh=False)
        self.solution_Ai = self.sim_Ai.solution

    def tearDown(self):
        os.remove("plot.png")

    def test_generate_summary_variables(self):
        generate_summary_variables(self.solution_Chen, self.chemistry_Chen2020)
        path = "plot.png"

        assert os.path.exists(path)

        generate_summary_variables(self.solution_Ai, self.chemistry_Ai2020)

        assert os.path.exists(path)


if __name__ == "__main__":
    unittest.main()
