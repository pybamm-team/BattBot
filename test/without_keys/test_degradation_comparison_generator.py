import unittest
import pybamm
from bot.plotting.degradation_comparison_generator import DegradationComparisonGenerator
import os


class TestDegradationComparisonGenerator(unittest.TestCase):
    def setUp(self):
        self.model = pybamm.lithium_ion.SPM(
            options={"SEI": "electron-migration limited"}
        )
        self.cycle = [
            (
                "Discharge at 2 C until 3.6 V",
                "Charge at 3 C until 3.8 V",
                "Hold at 3.8 V until 98 mA",
                "Rest for 4 minutes",
            )
        ]
        self.number = 2
        self.experiment = pybamm.Experiment(self.cycle * self.number)
        self.is_experiment = False
        self.degradation_parameter = "Inner SEI open-circuit potential [V]"
        self.varied_values = [0.09, 0.05]
        self.param_values_mohtat = []
        for i in range(2):
            self.param_values_mohtat.append(
                pybamm.ParameterValues("Mohtat2020")
            )
            self.param_values_mohtat[i][
                "Inner SEI open-circuit potential [V]"
            ] = self.varied_values[i]
        self.chemistry = "Mohtat2020"
        self.parameter_values = pybamm.ParameterValues(self.chemistry)

    def tearDown(self):
        os.remove("plot.png")

    def test_degradation_comparison_generator(self):
        degradation_comparison_generator = DegradationComparisonGenerator(
            self.model,
            self.chemistry,
            self.param_values_mohtat,
            self.degradation_parameter,
            self.cycle,
            self.number,
        )

        sim, solutions_and_labels = degradation_comparison_generator.create_simulation(
            self.experiment
        )

        self.assertIsNotNone(sim._solution)
        self.assertIsInstance(
            solutions_and_labels[0][0].all_models[0], pybamm.lithium_ion.SPM
        )
        self.assertEqual(
            sim.experiment.operating_conditions[0]["Current input [A]"],
            2 * self.parameter_values["Nominal cell capacity [A.h]"],
        )
        self.assertEqual(solutions_and_labels[0][0].termination, "final time")
        self.assertEqual(len(solutions_and_labels[0][0].cycles), 2)
        self.assertEqual(len(solutions_and_labels), 2)

        degradation_comparison_generator.solve()

        self.assertIsInstance(degradation_comparison_generator.solutions, list)
        self.assertIsInstance(degradation_comparison_generator.labels, list)
        for solution in degradation_comparison_generator.solutions:
            self.assertIsInstance(solution, pybamm.Solution)

        degradation_comparison_generator.generate_summary_variables()

        assert os.path.exists("plot.png")


if __name__ == "__main__":
    unittest.main()
