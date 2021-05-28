import unittest
import pybamm
from utils.chemistry_generator import chemistry_generator


class TestExperimentSolver(unittest.TestCase):

    def test_chemistry_generator_chen2020(self):
        (
        current_function,
        upper_voltage,
        lower_voltage,
        ambient_temp,
        initial_temp,
        reference_temp,
        ) = chemistry_generator(pybamm.parameter_sets.Chen2020)

        self.assertGreaterEqual(current_function, 1)
        self.assertLessEqual(current_function, 3)

        self.assertGreaterEqual(upper_voltage, 3.7)
        self.assertLessEqual(upper_voltage, 4.2)

        self.assertGreaterEqual(lower_voltage, 3.7)
        self.assertLessEqual(lower_voltage, 4.2)

        self.assertGreaterEqual(ambient_temp, 273.18)
        self.assertLessEqual(ambient_temp, 298.15)

        self.assertGreaterEqual(initial_temp, 273.18)
        self.assertLessEqual(initial_temp, 298.15)

        self.assertGreaterEqual(reference_temp, 273.18)
        self.assertLessEqual(reference_temp, 298.15)

    def test_chemistry_generator_marquis2019(self):
        (
        current_function,
        upper_voltage,
        lower_voltage,
        ambient_temp,
        initial_temp,
        reference_temp,
        ) = chemistry_generator(pybamm.parameter_sets.Marquis2019)

        self.assertGreaterEqual(current_function, 1)
        self.assertLessEqual(current_function, 5)

        self.assertGreaterEqual(upper_voltage, 3.1)
        self.assertLessEqual(upper_voltage, 4.1)

        self.assertGreaterEqual(lower_voltage, 3.1)
        self.assertLessEqual(lower_voltage, 4.1)

        self.assertGreaterEqual(ambient_temp, 273.18)
        self.assertLessEqual(ambient_temp, 298.15)

        self.assertGreaterEqual(initial_temp, 273.18)
        self.assertLessEqual(initial_temp, 298.15)

        self.assertGreaterEqual(reference_temp, 273.18)
        self.assertLessEqual(reference_temp, 298.15)

if __name__ == '__main__':
    unittest.main()