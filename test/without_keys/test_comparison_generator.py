import unittest
import pybamm
from bot.plotting.comparison_generator import ComparisonGenerator
import os


class TestComparisonGenerator(unittest.TestCase):
    def setUp(self):
        self.model_for_comp = {"DFN": pybamm.lithium_ion.DFN()}
        self.models_for_comp = {
            "DFN": pybamm.lithium_ion.DFN(),
            "SPM": pybamm.lithium_ion.SPM(),
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
        self.param_to_vary_info = {
            "Current function [A]": {"print_name": None, "bounds": (None, None)}
        }

    def tearDown(self):
        os.remove("plot.gif")

    def test_comparsion_generator(self):
        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary_info=self.param_to_vary_info,
        )

        comparison_generator.parameter_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
        )

        comparison_generator.model_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertTrue(len(comparison_generator.comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        self.is_experiment = True
        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            param_to_vary_info=self.param_to_vary_info,
        )

        comparison_generator.parameter_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=pybamm.parameter_sets.Ai2020,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            param_to_vary_info=self.param_to_vary_info,
        )

        comparison_generator.parameter_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=pybamm.parameter_sets.Ai2020,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
        )

        comparison_generator.model_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertTrue(len(comparison_generator.comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
        )

        comparison_generator.model_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertTrue(len(comparison_generator.comparison_dict["varied_values"]) == 0)
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        self.is_experiment = False

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary_info={
                "Negative electrode exchange-current density [A.m-2]": {
                    "print_name": r"$j_{0,n}$",
                    "bounds": (None, None),
                }
            },
        )

        comparison_generator.parameter_comparison()

        self.assertIsInstance(
            comparison_generator.comparison_dict["varied_values"], list
        )
        self.assertIsInstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")


if __name__ == "__main__":
    unittest.main()
