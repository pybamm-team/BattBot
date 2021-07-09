import unittest
import pybamm
from bot.experiment.experiment_solver import experiment_solver


class TestExperimentSolver(unittest.TestCase):
    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.experiment = pybamm.Experiment(
            [
                (
                    "Discharge at C/10 for 10 hours or until 3.3 V",
                    "Rest for 1 hour",
                    "Charge at 1 A until 4.1 V",
                    "Hold at 4.1 V until 50 mA",
                    "Rest for 1 hour",
                )
            ]
            * 3,
        )
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.solver = pybamm.CasadiSolver(mode="fast with events")
        self.parameter_values = pybamm.ParameterValues(
            chemistry=self.chemistry
        )
        self.param_values = [self.parameter_values]
        self.degradation_parameter = "Ambient temperature [K]"

    def test_experiment_solver(self):
        sim, solutions_and_labels, varied_values = experiment_solver(
            self.model,
            self.experiment,
            self.chemistry,
            self.solver,
            self.param_values,
            self.degradation_parameter
        )

        self.assertEqual(self.model.__class__, sim._model_class)
        self.assertFalse(sim._solution is None)
        self.assertEqual(sim.experiment, self.experiment)
        self.assertIsInstance(
            solutions_and_labels[0][0].all_models[0], pybamm.lithium_ion.DFN
        )
        self.assertEqual(
            sim._experiment_inputs[0]["Current input [A]"],
            1 / 10 * self.parameter_values["Nominal cell capacity [A.h]"],
        )
        self.assertEqual(solutions_and_labels[0][0].termination, "final time")
        self.assertEqual(len(solutions_and_labels[0][0].cycles), 3)
        self.assertEqual(len(solutions_and_labels), 1)
        self.assertIsInstance(varied_values, list)


if __name__ == "__main__":
    unittest.main()
