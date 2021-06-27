import unittest
import pybamm
from bot.utils.parameter_value_generator import parameter_value_generator
from bot.utils.parameter_value_generator import FunctionLike


class TextParameterValueGenerator(unittest.TestCase):
    def test_parameter_value_generator(self):

        parameter = "Lower voltage cut-off [V]"
        chemistry = pybamm.parameter_sets.Chen2020
        params = pybamm.ParameterValues(
            chemistry=chemistry
        )

        lower_voltage = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(lower_voltage, (params[parameter] - 0.1)*0.9)
        self.assertLessEqual(lower_voltage, (params[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        lower_voltage = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(lower_voltage, (params[parameter] - 0.1)*0.9)
        self.assertLessEqual(lower_voltage, (params[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Ai2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        lower_voltage = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(lower_voltage, (params[parameter] - 0.1)*0.9)
        self.assertLessEqual(lower_voltage, (params[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Yang2017
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        lower_voltage = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(lower_voltage, (params[parameter] - 0.1)*0.9)
        self.assertLessEqual(lower_voltage, (params[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        lower_voltage = parameter_value_generator(
            chemistry,
            parameter
        )

        self.assertGreaterEqual(lower_voltage, (params[parameter] - 0.1)*0.9)
        self.assertLessEqual(lower_voltage, (params[parameter] + 0.1)*1.1)

        parameter = "Negative electrode exchange-current density [A.m-2]"
        base_value = {}
        base_value[parameter] = 1.0

        chemistry = pybamm.parameter_sets.Chen2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        current = parameter_value_generator(
            chemistry,
            parameter
        )

        params[parameter] = FunctionLike(params[parameter], parameter)
        self.assertGreaterEqual(current, (base_value[parameter] - 0.1)*0.9)
        self.assertLessEqual(current, (base_value[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Marquis2019
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        current = parameter_value_generator(
            chemistry,
            parameter
        )

        params[parameter] = FunctionLike(params[parameter], parameter)
        self.assertGreaterEqual(current, (base_value[parameter] - 0.1)*0.9)
        self.assertLessEqual(current, (base_value[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Ai2020
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        current = parameter_value_generator(
            chemistry,
            parameter
        )

        params[parameter] = FunctionLike(params[parameter], parameter)
        self.assertGreaterEqual(current, (base_value[parameter] - 0.1)*0.9)
        self.assertLessEqual(current, (base_value[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Yang2017
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        current = parameter_value_generator(
            chemistry,
            parameter
        )

        params[parameter] = FunctionLike(params[parameter], parameter)
        self.assertGreaterEqual(current, (base_value[parameter] - 0.1)*0.9)
        self.assertLessEqual(current, (base_value[parameter] + 0.1)*1.1)

        chemistry = pybamm.parameter_sets.Chen2020_plating
        params = params = pybamm.ParameterValues(
            chemistry=chemistry
        )
        current = parameter_value_generator(
            chemistry,
            parameter
        )

        params[parameter] = FunctionLike(params[parameter], parameter)
        self.assertGreaterEqual(current, (base_value[parameter] - 0.1)*0.9)
        self.assertLessEqual(current, (base_value[parameter] + 0.1)*1.1)


if __name__ == "__main__":
    unittest.main()
