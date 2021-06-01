import unittest
import pybamm
from bot.plotting.random_plot_generator import random_plot_generator


class TestTweetPlot(unittest.TestCase):
    def test_tweet_graph(self):
        (
            model,
            parameter_values,
            time,
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
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time, int)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertFalse(is_comparison)

        (
            model,
            parameter_values,
            time,
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
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsNone(time)
        self.assertIsNotNone(cycle)
        self.assertIsNotNone(number)
        self.assertTrue(is_experiment)
        self.assertFalse(is_comparison)
        pybamm.Experiment(cycle * number)

        (
            model,
            parameter_values,
            time,
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
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsInstance(solver, pybamm.BaseSolver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time, int)
        self.assertIsNotNone(cycle)
        self.assertIsNotNone(number)
        self.assertTrue(is_experiment)
        self.assertFalse(is_comparison)
        pybamm.Experiment(cycle * number)

        (
            models,
            parameter_values,
            time,
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
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsNone(solver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time, int)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertTrue(is_comparison)

        (
            models,
            parameter_values,
            time,
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
        self.assertEqual("lithium_ion", chemistry["chemistry"])
        self.assertIsNone(solver)
        self.assertIsInstance(parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(time, int)
        self.assertIsNone(cycle)
        self.assertIsNone(number)
        self.assertFalse(is_experiment)
        self.assertTrue(is_comparison)


if __name__ == "__main__":
    unittest.main()
