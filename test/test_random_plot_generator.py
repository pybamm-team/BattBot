import unittest
import pybamm
import multiprocessing
from bot.plotting.random_plot_generator import random_plot_generator
import os


class TestRandomPlotGenerator(unittest.TestCase):

    def tearDown(self):
        os.remove("plot.png")
        os.remove("plot.gif")

    def test_random_plot_generator(self):

        key_list = [
            "particle mechanics",
            "lithium plating",
            "SEI",
            "lithium plating porosity change"
        ]

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": 0,
                        "chemistry": pybamm.parameter_sets.Ai2020,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(
            key in key_list for key in return_dict["model"].options.keys()
        )
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertTrue(
            return_dict["solver"] == "CasADi solver with 'safe' mode"
            or return_dict["solver"] == "CasADi solver with 'fast' mode"
            or return_dict["solver"] == (
                "CasADi solver with 'fast with events' mode"
            )
        )
        self.assertIsInstance(
            return_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(return_dict["time_array"], list)
        self.assertTrue(len(return_dict["time_array"]) == 2)
        self.assertIsNone(return_dict["cycle"])
        self.assertIsNone(return_dict["number"])
        self.assertFalse(return_dict["is_experiment"])
        self.assertFalse(return_dict["is_comparison"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": 1,
                        "chemistry": pybamm.parameter_sets.Chen2020,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(
            key in key_list for key in return_dict["model"].options.keys()
        )
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertTrue(
            return_dict["solver"] == "CasADi solver with 'safe' mode"
            or return_dict["solver"] == "CasADi solver with 'fast' mode"
            or return_dict["solver"] == (
                "CasADi solver with 'fast with events' mode"
            )
        )
        self.assertIsInstance(
            return_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsNone(return_dict["time_array"])
        self.assertIsNotNone(return_dict["cycle"])
        self.assertIsNotNone(return_dict["number"])
        self.assertTrue(return_dict["is_experiment"])
        self.assertFalse(return_dict["is_comparison"])
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": 2,
                        "chemistry": pybamm.parameter_sets.Yang2017,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(
            key in key_list for key in return_dict["model"].options.keys()
        )
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertTrue(
            return_dict["solver"] == "CasADi solver with 'safe' mode"
            or return_dict["solver"] == "CasADi solver with 'fast' mode"
            or return_dict["solver"] == (
                "CasADi solver with 'fast with events' mode"
            )
        )
        self.assertIsInstance(
            return_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsNone(return_dict["time_array"])
        self.assertIsNotNone(return_dict["cycle"])
        self.assertIsNotNone(return_dict["number"])
        self.assertTrue(return_dict["is_experiment"])
        self.assertFalse(return_dict["is_comparison"])
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": 3,
                        "chemistry": None,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                p.kill()
                p.join()
            else:
                break

        for model in return_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
            self.assertIsNotNone(model.options)
            self.assertIsInstance(model.options, dict)
            self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertIsNone(return_dict["solver"])
        self.assertIsInstance(
            return_dict["parameter_values"], pybamm.ParameterValues
        )
        self.assertIsInstance(return_dict["time_array"], list)
        self.assertTrue(len(return_dict["time_array"]) == 2)
        self.assertIsNone(return_dict["cycle"])
        self.assertIsNone(return_dict["number"])
        self.assertFalse(return_dict["is_experiment"])
        self.assertTrue(return_dict["is_comparison"])


if __name__ == "__main__":
    unittest.main()
