import unittest
import pybamm
import multiprocessing
from bot.plotting.random_plot_generator import random_plot_generator
import os


class TestRandomPlotGenerator(unittest.TestCase):
    def tearDown(self):
        if os.path.exists("plot.png"):
            os.remove("plot.png")
        if os.path.exists("plot.gif"):
            os.remove("plot.gif")

    def test_random_plot_generator(self):

        key_list = [
            "particle mechanics",
            "lithium plating",
            "SEI",
            "lithium plating porosity change",
        ]

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator,
                args=(
                    return_dict,
                    "degradation comparison (summary variables)",
                ),
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(key in key_list for key in return_dict["model"].options.keys())
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertIsNotNone(return_dict["cycle"])
        self.assertIsNotNone(return_dict["number"])
        self.assertTrue(return_dict["is_experiment"])
        self.assertFalse(return_dict["is_comparison"])
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(return_dict, "model comparison")
            )
            p.start()
            p.join(1200)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
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
        self.assertIsInstance(return_dict["is_experiment"], bool)
        self.assertIsInstance(return_dict["is_comparison"], bool)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(return_dict, "parameter comparison")
            )
            p.start()
            p.join(1200)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
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
        self.assertIsInstance(return_dict["is_experiment"], bool)
        self.assertIsInstance(return_dict["is_comparison"], bool)


if __name__ == "__main__":
    unittest.main()
