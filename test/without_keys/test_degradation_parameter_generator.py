import pybamm
import unittest
from bot.utils.degradation_parameter_generator import (
    degradation_parameter_generator,
    lico2_volume_change_Ai2020,
    graphite_volume_change_Ai2020,
)


class TestDegradationParameterGenerator(unittest.TestCase):
    def test_degradation_parameter_generator(self):

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Ai2020,
            2,
            degradation_mode="particle mechanics",
            degradation_value="swelling and cracking",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="reaction limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="ec reaction limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="solvent-diffusion limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="electron-migration limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="interstitial-diffusion limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Mohtat2020,
            2,
            degradation_mode="SEI",
            degradation_value="interstitial-diffusion limited",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            pybamm.parameter_sets.Mohtat2020,
            2,
            degradation_mode="particle mechanics",
            degradation_value="swelling only",
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        t_change = lico2_volume_change_Ai2020(5, 3)
        self.assertIsInstance(
            t_change, pybamm.expression_tree.binary_operators.Multiplication
        )
        t_change = graphite_volume_change_Ai2020(5, 1)
        self.assertEqual(t_change, 103545409.4049503)


if __name__ == "__main__":
    unittest.main()
