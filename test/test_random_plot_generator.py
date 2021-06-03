import unittest
import pybamm
from bot.plotting.random_plot_generator import random_plot_generator
import os


class TestTweetPlot(unittest.TestCase):

    def tearDown(self):
        os.remove("plot.png")
        os.remove("plot.gif")

    def test_tweet_graph(self):

        key_list = [
            "particle mechanics",
            "lithium plating",
            "SEI",
            "lithium plating porosity change"
        ]

        (
            model,
            parameter_values,
            time_array,
            chemistry,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison,
        ) = random_plot_generator(
            testing=True,
            provided_choice=0
        )

        self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsNotNone(model.options)
        self.assertIsInstance(model.options, dict)
        self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time_array, list)
        self.assertTrue(len(time_array) == 2)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertFalse(is_comparison)

        (
            model,
            parameter_values,
            time_array,
            chemistry,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison,
        ) = random_plot_generator(
            testing=True,
            provided_choice=1
        )

        self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsNotNone(model.options)
        self.assertIsInstance(model.options, dict)
        self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsNone(time_array)
        self.assertIsNotNone(cycle)
        self.assertIsNotNone(number)
        self.assertTrue(is_experiment)
        self.assertFalse(is_comparison)
        pybamm.Experiment(cycle * number)

        (
            model,
            parameter_values,
            time_array,
            chemistry,
            solver,
            isExperiment,
            cycle,
            number,
            isComparison,
        ) = random_plot_generator(
            testing=True,
            provided_choice=1,
            plot_summary_variables=False
        )

        self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsNotNone(model.options)
        self.assertIsInstance(model.options, dict)
        self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time_array, list)
        self.assertTrue(len(time_array) == 2)
        self.assertIsNotNone(cycle)
        self.assertIsNotNone(number)
        self.assertTrue(is_experiment)
        self.assertFalse(is_comparison)
        pybamm.Experiment(cycle * number)

        (
            models,
            parameter_values,
            time_array,
            chemistry,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison,
        ) = random_plot_generator(
            testing=True,
            provided_choice=2
        )

        for model in models.values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
            self.assertIsNotNone(model.options)
            self.assertIsInstance(model.options, dict)
            self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsNone(solver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time_array, list)
        self.assertTrue(len(time_array) == 2)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertTrue(is_comparison)

        (
            models,
            parameter_values,
            time_array,
            chemistry,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison,
        ) = random_plot_generator(
            testing=True,
            provided_choice=2,
            provided_number_of_comp=1
        )

        for model in models.values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
            self.assertIsNotNone(model.options)
            self.assertIsInstance(model.options, dict)
            self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsNone(solver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time_array, list)
        self.assertTrue(len(time_array) == 2)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertTrue(is_comparison)


if __name__ == "__main__":
    unittest.main()
