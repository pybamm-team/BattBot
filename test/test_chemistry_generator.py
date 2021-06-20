import unittest
import pybamm
from bot.utils.chemistry_generator import chemistry_generator


class TestChemistryGenerator(unittest.TestCase):
    def test_chemistry_generator(self):
        lower_voltage = chemistry_generator(
            pybamm.parameter_sets.Chen2020,
            "Lower voltage cut-off [V]"
        )

        self.assertGreaterEqual(lower_voltage, 2.5)
        self.assertLessEqual(lower_voltage, 4.0)

        lower_voltage = chemistry_generator(
            pybamm.parameter_sets.Marquis2019,
            "Lower voltage cut-off [V]"
        )

        self.assertGreaterEqual(lower_voltage, 3.1)
        self.assertLessEqual(lower_voltage, 3.9)

        lower_voltage = chemistry_generator(
            pybamm.parameter_sets.Ai2020,
            "Lower voltage cut-off [V]"
        )

        self.assertGreaterEqual(lower_voltage, 2.7)
        self.assertLessEqual(lower_voltage, 3.9)

        lower_voltage = chemistry_generator(
            pybamm.parameter_sets.Yang2017,
            "Lower voltage cut-off [V]"
        )

        self.assertGreaterEqual(lower_voltage, 2.7)
        self.assertLessEqual(lower_voltage, 3.9)

        lower_voltage = chemistry_generator(
            pybamm.parameter_sets.Chen2020_plating,
            "Lower voltage cut-off [V]"
        )

        self.assertGreaterEqual(lower_voltage, 2.7)
        self.assertLessEqual(lower_voltage, 3.9)

        current = chemistry_generator(
            pybamm.parameter_sets.Chen2020,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 3)
        self.assertLessEqual(current, 5)

        current = chemistry_generator(
            pybamm.parameter_sets.Marquis2019,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.1)
        self.assertLessEqual(current, 0.65)

        current = chemistry_generator(
            pybamm.parameter_sets.Ai2020,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.5)
        self.assertLessEqual(current, 2.25)

        current = chemistry_generator(
            pybamm.parameter_sets.Yang2017,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 0.5)
        self.assertLessEqual(current, 2.25)

        current = chemistry_generator(
            pybamm.parameter_sets.Chen2020_plating,
            "Current function [A]"
        )

        self.assertGreaterEqual(current, 3)
        self.assertLessEqual(current, 5)


if __name__ == "__main__":
    unittest.main()
