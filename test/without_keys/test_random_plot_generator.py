import multiprocessing
import os
import unittest

import pybamm
from bot.plotting.random_plot_generator import random_plot_generator


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

        model = pybamm.lithium_ion.DFN()
        cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        number = 2
        chemistry = "Chen2020"
        degradation_parameter = "Ambient temperature [K]"

        param_values = []
        for i in range(2):
            param_values.append(pybamm.ParameterValues("Chen2020"))
            param_values[i]["Ambient temperature [K]"] = [290, 285, 295][i]

        return_dict = {}
        random_plot_generator(
            return_dict,
            "degradation comparison",
            {
                "model": model,
                "cycle": cycle,
                "number": number,
                "chemistry": chemistry,
                "degradation_parameter": degradation_parameter,
                "varied_values": [290, 285, 295],
                "param_values": param_values,
                "degradation_mode": "SEI",
                "degradation_value": "reaction limited",
            },
            testing=True,
        )

        assert return_dict["model"] == model
        assert return_dict["model"].options is not None
        assert isinstance(return_dict["model"].options, dict)
        assert (key in key_list for key in return_dict["model"].options)
        assert return_dict["chemistry"] == chemistry
        assert return_dict["cycle"] == cycle
        assert return_dict["number"] == number
        assert return_dict["is_experiment"]
        assert not return_dict["is_comparison"]
        assert isinstance(return_dict["param_to_vary"], str)
        assert return_dict["degradation_mode"] == "SEI"
        assert return_dict["degradation_value"] == "reaction limited"
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator,
                args=(return_dict, "degradation comparison", None, True),
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long,",
                    "KILLING IT and starting a NEW ONE.",
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
                p.kill()
                p.join()
            else:
                break

        assert isinstance(return_dict["model"], pybamm.BaseBatteryModel)
        assert return_dict["model"].options is not None
        assert isinstance(return_dict["model"].options, dict)
        assert (key in key_list for key in return_dict["model"].options)
        assert return_dict["cycle"] is not None
        assert return_dict["number"] is not None
        assert return_dict["is_experiment"]
        assert not return_dict["is_comparison"]
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        model = pybamm.lithium_ion.DFN()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator,
                args=(return_dict, "model comparison", None, True),
            )
            p.start()
            p.join(1200)

            if p.is_alive():
                print(
                    "Simulation is taking too long,",
                    "KILLING IT and starting a NEW ONE.",
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
            assert isinstance(model, pybamm.BaseBatteryModel)
            assert model.options is not None
            assert isinstance(model.options, dict)
            assert (key in key_list for key in model.options)
        assert isinstance(return_dict["is_experiment"], bool)
        assert isinstance(return_dict["is_comparison"], bool)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator,
                args=(return_dict, "parameter comparison", None, True),
            )
            p.start()
            p.join(1200)

            if p.is_alive():
                print(
                    "Simulation is taking too long,",
                    "KILLING IT and starting a NEW ONE.",
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
            assert isinstance(model, pybamm.BaseBatteryModel)
            assert model.options is not None
            assert isinstance(model.options, dict)
            assert (key in key_list for key in model.options)
        assert isinstance(return_dict["is_experiment"], bool)
        assert isinstance(return_dict["is_comparison"], bool)


if __name__ == "__main__":
    unittest.main()
