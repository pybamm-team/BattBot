import unittest
import pybamm
from bot.utils.parameter_value_generator import parameter_value_generator


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

        current = parameter_value_generator(
            pybamm.parameter_sets.Chen2020,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 3)
        self.assertLessEqual(current, 5)

        current = parameter_value_generator(
            pybamm.parameter_sets.Marquis2019,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.1)
        self.assertLessEqual(current, 0.65)

        current = parameter_value_generator(
            pybamm.parameter_sets.Ai2020,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.5)
        self.assertLessEqual(current, 2.25)

        current = parameter_value_generator(
            pybamm.parameter_sets.Yang2017,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.5)
        self.assertLessEqual(current, 2.25)

        current = parameter_value_generator(
            pybamm.parameter_sets.Chen2020_plating,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 3)
        self.assertLessEqual(current, 5)


if __name__ == "__main__":
    unittest.main()
