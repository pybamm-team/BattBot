import pybamm
import unittest
from bot.utils.degradation_parameter_generator import (
    degradation_parameter_generator
)


class TestDegradationParameterGenerator(unittest.TestCase):
    def test_degradation_parameter_generator(self):

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Ai2020,
            2,
            degradation_mode="particle mechanics",
            degradation_value="swelling and cracking"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="reaction limited"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="ec reaction limited"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="solvent-diffusion limited"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="electron-migration limited"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)

        (
            param_values,
            degradation_parameter
        ) = degradation_parameter_generator(
            pybamm.parameter_sets.Chen2020,
            2,
            degradation_mode="SEI",
            degradation_value="interstitial-diffusion limited"
        )
        self.assertIsInstance(param_values, list)
        self.assertIsInstance(param_values[0], pybamm.ParameterValues)
        self.assertEqual(len(param_values), 2)
        self.assertIsInstance(degradation_parameter, str)


if __name__ == "__main__":
    unittest.main()
