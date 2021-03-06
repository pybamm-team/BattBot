import unittest
from bot.utils.desired_decimal_point_generator import (
    desired_decimal_point_generator
)


class TestExperimentSolver(unittest.TestCase):
    def test_desired_decimal_point_generator(self):
        num = desired_decimal_point_generator(0, 5, 1)

        self.assertGreaterEqual(num, 0)
        self.assertLessEqual(num, 5)


if __name__ == "__main__":
    unittest.main()
