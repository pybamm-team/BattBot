import unittest
import pybamm
from bot.utils.parameter_value_generator import parameter_value_generator


class TestParameterValueGenerator(unittest.TestCase):
    def test_parameter_value_generator(self):

        parameter = {"Lower voltage cut-off [V]": (None, None)}
        chemistry = pybamm.parameter_sets.Chen2020
        params = pybamm.ParameterValues(chemistry=chemistry)

        new_params = parameter_value_generator(params, parameter)

        self.assertGreaterEqual(
            new_params[list(parameter.keys())[0]],
            params[list(parameter.keys())[0]] * 0.5,
        )
        self.assertLessEqual(
            new_params[list(parameter.keys())[0]], params[list(parameter.keys())[0]] * 2
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertGreaterEqual(
            new_params[list(parameter.keys())[0]],
            params[list(parameter.keys())[0]] * 0.5,
        )
        self.assertLessEqual(
            new_params[list(parameter.keys())[0]], params[list(parameter.keys())[0]] * 2
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Ai2020
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertGreaterEqual(
            new_params[list(parameter.keys())[0]],
            params[list(parameter.keys())[0]] * 0.5,
        )
        self.assertLessEqual(
            new_params[list(parameter.keys())[0]], params[list(parameter.keys())[0]] * 2
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertGreaterEqual(
            new_params[list(parameter.keys())[0]],
            params[list(parameter.keys())[0]] * 0.5,
        )
        self.assertLessEqual(
            new_params[list(parameter.keys())[0]], params[list(parameter.keys())[0]] * 2
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        parameter = {
            "Negative electrode exchange-current density [A.m-2]": (None, None)
        }

        chemistry = pybamm.parameter_sets.Chen2020
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertIsInstance(
            int(new_param["Negative electrode exchange-current density [A.m-2]"]), int
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertIsInstance(
            int(new_param["Negative electrode exchange-current density [A.m-2]"]), int
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Ai2020
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertIsInstance(
            int(new_param["Negative electrode exchange-current density [A.m-2]"]), int
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertIsInstance(
            int(new_param["Negative electrode exchange-current density [A.m-2]"]), int
        )
        self.assertIsInstance(new_params, pybamm.ParameterValues)

        parameter = {"Negative electrode diffusivity [m2.s-1]": (None, None)}
        chemistry = pybamm.parameter_sets.Chen2020
        params = pybamm.ParameterValues(chemistry=chemistry)
        new_params = parameter_value_generator(params, parameter)

        self.assertIsInstance(new_params, pybamm.ParameterValues)


if __name__ == "__main__":
    unittest.main()
