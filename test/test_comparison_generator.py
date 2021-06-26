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
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            provided_choice="no experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            1,
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            provided_choice= "experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        self.assertEqual(comparison_dict["model"], self.model_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)

        assert os.path.exists("plot.gif")

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=pybamm.parameter_sets.Ai2020,
            provided_choice="experiment"
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(
            comparison_dict["chemistry"], pybamm.parameter_sets.Ai2020
        )

        comparison_dict = comparison_generator(
            2,
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
        )

        self.assertIsInstance(comparison_dict, dict)
        self.assertIsInstance(comparison_dict["model"], dict)
        self.assertEqual(comparison_dict["model"], self.models_for_comp)
        self.assertIsInstance(
            comparison_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(comparison_dict["time_array"], list)
        self.assertEqual(len(comparison_dict["time_array"]), 2)
        self.assertEqual(comparison_dict["chemistry"], self.chemistry)


if __name__ == "__main__":
    unittest.main()
