import unittest
import pybamm
from models.model_generator import model_generator


class TestSolvingModel(unittest.TestCase):

    def setUp(self):
        self.model = pybamm.lithium_ion.DFN()
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.solver = pybamm.CasadiSolver(mode="fast with events")

    def test_model_solver(self):
        parameter_values, sim, solution = model_generator(
            self.model,
            self.chemistry,
            self.solver,
            5.0,
            2.7,
            4.1,
            298,
            298,
            298,
        )

        self.assertEqual(self.model.__class__, sim._model_class)
        self.assertFalse(sim._solution is None)
        self.assertIsInstance(solution.all_models[0], pybamm.lithium_ion.DFN)
        self.assertEqual(parameter_values["Current function [A]"], 5.0)
        self.assertEqual(parameter_values["Lower voltage cut-off [V]"], 2.7)
        self.assertEqual(parameter_values["Upper voltage cut-off [V]"], 4.1)
        self.assertEqual(parameter_values["Ambient temperature [K]"], 298)
        self.assertEqual(parameter_values["Initial temperature [K]"], 298)
        self.assertEqual(parameter_values["Reference temperature [K]"], 298)

if __name__ == '__main__':
    unittest.main()