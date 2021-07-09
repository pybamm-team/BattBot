import unittest
import pybamm
from bot.utils.parameter_value_generator import parameter_value_generator


class TestParameterValueGenerator(unittest.TestCase):
    def test_parameter_value_generator(self):

        parameter = "Lower voltage cut-off [V]"
        chemistry = pybamm.parameter_sets.Chen2020
        params = pybamm.ParameterValues(
            chemistry=chemistry
        )

        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(new_params[parameter], params[parameter]*0.5)
        self.assertLessEqual(new_params[parameter], params[parameter]*2)
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(new_params[parameter], params[parameter]*0.5)
        self.assertLessEqual(new_params[parameter], params[parameter]*2)
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Ai2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(new_params[parameter], params[parameter]*0.5)
        self.assertLessEqual(new_params[parameter], params[parameter]*2)
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Yang2017
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(new_params[parameter], params[parameter]*0.5)
        self.assertLessEqual(new_params[parameter], params[parameter]*2)
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(new_params[parameter], params[parameter]*0.5)
        self.assertLessEqual(new_params[parameter], params[parameter]*2)
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        parameter = "Negative electrode exchange-current density [A.m-2]"
        base_value = {}
        base_value[parameter] = 1.0

        chemistry = pybamm.parameter_sets.Chen2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Ai2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Yang2017
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        new_params = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertIsInstance(new_params, pybamm.ParameterValues)


if __name__ == "__main__":
    unittest.main()
