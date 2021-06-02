import unittest
import pybamm
from bot.information.information import information


class TestInformation(unittest.TestCase):
    def setUp(self):
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.model = pybamm.lithium_ion.DFN()
        self.solver = pybamm.CasadiSolver(mode="fast with events")
        self.is_experiment = True
        self.cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        self.number = 3
        self.is_comparison = False

    def test_information(self):
        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
        )

        self.assertEqual(
            result,
            "[('Discharge at C/10 for 10 hours or until 3.3 V', "
            + "'Rest for 1 hour', 'Charge at 1 A until 4.1 V', "
            + "'Hold at 4.1 V until 50 mA', 'Rest for "
            + "1 hour')] * 3 Doyle-Fuller-Newman model Chen2020",
        )

        self.is_comparison = True
        self.is_experiment = False
        self.model = {
            "DFN": pybamm.lithium_ion.DFN()
        }

        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
        )

        self.assertEqual(result, "Chen2020")
        self.is_comparison = False
        self.model = pybamm.lithium_ion.DFN()

        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
        )

        self.assertEqual(
            result,
            "Doyle-Fuller-Newman model Chen2020 "
            + "CasADi solver with 'fast with events' mode"
        )


if __name__ == "__main__":
    unittest.main()
