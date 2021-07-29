import unittest
import pybamm
from bot.plotting.comparison_generator import ComparisonGenerator
import os


class TestComparisonGenerator(unittest.TestCase):

    def setUp(self):
        self.model_for_comp = {
            "DFN": pybamm.lithium_ion.DFN()
        }
        self.models_for_comp = {
            "DFN": pybamm.lithium_ion.DFN(),
            "SPM": pybamm.lithium_ion.SPM()
        }
        self.chemistry = pybamm.parameter_sets.Chen2020
        self.cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        self.number = 1
        self.is_experiment = False
        self.param_to_vary = "Current function [A]"
        self.param_to_vary_dict = {
            "Current function [A]": (None, None),
            "Electrode height [m]": (0.1, None),
            "Electrode width [m]": (0.1, None),
            "Negative electrode conductivity [S.m-1]": (None, None),
            "Negative electrode porosity": (None, None),
            "Negative electrode active material volume fraction": (None, None),
            "Negative electrode Bruggeman coefficient (electrolyte)":
            (None, None),
            "Negative electrode exchange-current density [A.m-2]":
            (None, None),
            "Positive electrode porosity": (None, None),
            "Positive electrode exchange-current density [A.m-2]":
            (None, None),
            "Positive electrode Bruggeman coefficient (electrolyte)":
            (None, None),
            "Ambient temperature [K]": (265, 355),
        }

    def tearDown(self):
        os.remove("plot.gif")

    def test_comparsion_generator(self):
        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary=self.param_to_vary,
            bounds=self.param_to_vary_dict[self.param_to_vary]
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertTrue(len(comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertTrue(len(comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        self.is_experiment = True
        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            param_to_vary=self.param_to_vary,
            bounds=self.param_to_vary_dict[self.param_to_vary]
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=pybamm.parameter_sets.Ai2020,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertTrue(len(comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_dict["params"], dict)

        self.is_experiment = False

        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary="Negative electrode exchange-current density [A.m-2]",    # noqa
            bounds=self.param_to_vary_dict[self.param_to_vary]
        )

        self.assertIsInstance(comparison_dict["varied_values"], list)
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")


if __name__ == "__main__":
    unittest.main()
