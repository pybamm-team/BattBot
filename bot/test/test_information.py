import unittest
import pybamm
from information.information import information


class TestInformation(unittest.TestCase):
    def setUp(self):
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.model = pybamm.lithium_ion.DFN()
        self.solver = pybamm.CasadiSolver(mode="fast with events")
        self.isExperiment = True
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
        self.isComparison = False

    def test_information(self):
        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.isExperiment,
            self.cycle,
            self.number,
            self.isComparison
        )

        self.assertEqual(
            str(self.cycle) + " * " + str(self.number),
            result.split('<')[0].strip()
        )
        self.assertEqual(
            str(self.chemistry["citation"]),
            result.split('>')[1].strip()
        )
        self.assertEqual("dfn", result.split('.')[7].strip())

        self.isComparison = True
        self.isExperiment = False

        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.isExperiment,
            self.cycle,
            self.number,
            self.isComparison
        )

        self.isComparison = False
        self.assertEqual("dfn", result.split('.')[4].strip())

        result = information(
            self.chemistry,
            self.model,
            self.solver,
            self.isExperiment,
            self.cycle,
            self.number,
            self.isComparison
        )

        self.assertEqual(
            str(self.chemistry["citation"]),
            result.split('>')[1].split('<')[0].strip()
        )
        self.assertEqual(
            "casadi_solver",
            result.split('>')[1].split('<')[1].split('.')[2].strip()
        )
        self.assertEqual("dfn", result.split('.')[4].strip())


if __name__ == "__main__":
    unittest.main()
