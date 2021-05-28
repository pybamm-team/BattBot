import unittest
import pybamm
from utils.single_point_decimal import single_decimal_point


class TestExperimentSolver(unittest.TestCase):

    def test_single_decimal_point(self):
        num = single_decimal_point(0, 5, 0.1)

        self.assertGreaterEqual(num, 0)
        self.assertLessEqual(num, 5)

if __name__ == '__main__':
    unittest.main()