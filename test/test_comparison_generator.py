import unittest
import pybamm
from bot.plotting.comparison_generator import comparison_generator
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

    def tearDown(self):
        os.remove("plot.gif")

    def test_comparsion_generator(self):
        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertIsNone(comparison_dict["cycle"])
        self.assertIsNone(comparison_dict["number"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNotNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertIsNone(comparison_dict["cycle"])
        self.assertIsNone(comparison_dict["number"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertIsNone(comparison_dict["cycle"])
        self.assertIsNone(comparison_dict["number"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            provided_choice="experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertEqual(comparison_dict["number"], 1)
        self.assertEqual(
            comparison_dict["cycle"],
            [
                (
                    "Discharge at C/10 for 10 hours "
                    + "or until 3.3 V",
                    "Rest for 1 hour",
                    "Charge at 1 A until 4.1 V",
                    "Hold at 4.1 V until 50 mA",
                    "Rest for 1 hour"
                )
            ]
        )
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNotNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=pybamm.parameter_sets.Ai2020,
            provided_choice="experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertEqual(comparison_dict["number"], 1)
        self.assertEqual(
            comparison_dict["cycle"],
            [
                (
                    "Discharge at C/10 for 10 hours "
                    + "or until 3.3 V",
                    "Rest for 1 hour",
                    "Charge at 1 A until 4.1 V",
                    "Hold at 4.1 V until 50 mA",
                    "Rest for 1 hour"
                )
            ]
        )
        self.assertEqual(
            comparison_dict["chemistry"], pybamm.parameter_sets.Ai2020
        )
        self.assertIsNone(comparison_dict["param_to_vary"])

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment",
            provided_param_to_vary="Current function [A]"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertIsNone(comparison_dict["cycle"])
        self.assertIsNone(comparison_dict["number"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNotNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment",
            provided_param_to_vary="Electrode height [m]"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        for model in comparison_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseModel)
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertTrue(comparison_dict["is_comparison"])
        self.assertIsNone(comparison_dict["cycle"])
        self.assertIsNone(comparison_dict["number"])
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)
        self.assertIsNotNone(comparison_dict["param_to_vary"])
        self.assertIsInstance(comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")


if __name__ == "__main__":
    unittest.main()
