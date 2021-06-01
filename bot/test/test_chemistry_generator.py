import unittest
import pybamm
from utils.chemistry_generator import chemistry_generator


class TestExperimentSolver(unittest.TestCase):
    def test_chemistry_generator_chen2020(self):
        lower_voltage = chemistry_generator(pybamm.parameter_sets.Chen2020)

        self.assertGreaterEqual(lower_voltage, 2.5)
        self.assertLessEqual(lower_voltage, 4.0)

    def test_chemistry_generator_marquis2019(self):
        lower_voltage = chemistry_generator(pybamm.parameter_sets.Marquis2019)

        self.assertGreaterEqual(lower_voltage, 3.1)
        self.assertLessEqual(lower_voltage, 3.9)


if __name__ == "__main__":
    unittest.main()
