import unittest
import pybamm
from bot.plotting.config_generator import config_generator


class TestConfigGenerator(unittest.TestCase):
    def test_config_generator(self):
        config = config_generator("degradation comparison")

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["model"], pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["cycle"], list)
        self.assertIsInstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        self.assertIsInstance(config["degradation_parameter"], str)
        self.assertIsInstance(config["degradation_mode"], str)
        self.assertIsInstance(config["degradation_value"], str)
        self.assertIsInstance(config["varied_values"], list)
        self.assertIsInstance(config["param_values"], list)
        for param in config["param_values"]:
            self.assertIsInstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": pybamm.parameter_sets.Ai2020,
                "is_experiment": None,
                "number_of_comp": None,
            },
        )

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["model"], pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["cycle"], list)
        self.assertIsInstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        self.assertIsInstance(config["degradation_parameter"], str)
        self.assertIsInstance(config["degradation_mode"], str)
        self.assertIsInstance(config["degradation_value"], str)
        self.assertIsInstance(config["varied_values"], list)
        self.assertIsInstance(config["param_values"], list)
        for param in config["param_values"]:
            self.assertIsInstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": pybamm.parameter_sets.Mohtat2020,
                "is_experiment": None,
                "number_of_comp": None,
            },
        )

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["model"], pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["cycle"], list)
        self.assertIsInstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        self.assertIsInstance(config["degradation_parameter"], str)
        self.assertIsInstance(config["degradation_mode"], str)
        self.assertIsInstance(config["degradation_value"], str)
        self.assertIsInstance(config["varied_values"], list)
        self.assertIsInstance(config["param_values"], list)
        for param in config["param_values"]:
            self.assertIsInstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": pybamm.parameter_sets.Chen2020,
                "is_experiment": None,
                "number_of_comp": None,
            },
        )

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["model"], pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["cycle"], list)
        self.assertIsInstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        self.assertIsInstance(config["degradation_parameter"], str)
        self.assertIsInstance(config["degradation_mode"], str)
        self.assertIsInstance(config["degradation_value"], str)
        self.assertIsInstance(config["varied_values"], list)
        self.assertIsInstance(config["param_values"], list)
        for param in config["param_values"]:
            self.assertIsInstance(param, pybamm.ParameterValues)

        config = config_generator("parameter comparison")

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["is_experiment"], bool)
        self.assertTrue(isinstance(config["cycle"], list) or config["cycle"] is None)
        self.assertTrue(isinstance(config["number"], int) or config["number"] is None)
        self.assertTrue(isinstance(config["param_to_vary_info"], dict))

        config = config_generator("model comparison")

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["is_experiment"], bool)
        self.assertTrue(isinstance(config["cycle"], list) or config["cycle"] is None)
        self.assertTrue(isinstance(config["number"], int) or config["number"] is None)
        self.assertIsNone(config["param_to_vary_info"])

        config = config_generator(
            "parameter comparison",
            test_config={"chemistry": None, "is_experiment": True, "number_of_comp": 1},
        )

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["is_experiment"], bool)
        self.assertTrue(config["is_experiment"])
        self.assertIsInstance(config["cycle"], list)
        self.assertIsInstance(config["number"], int)
        self.assertIsInstance(config["param_to_vary_info"], dict)

        config = config_generator(
            "model comparison",
            test_config={
                "chemistry": None,
                "is_experiment": False,
                "number_of_comp": 2,
            },
        )

        self.assertIsInstance(config, dict)
        self.assertIsInstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
        self.assertIsInstance(config["chemistry"], dict)
        self.assertIsInstance(config["is_experiment"], bool)
        self.assertFalse(config["is_experiment"])
        self.assertIsNone(config["cycle"])
        self.assertIsNone(config["number"])
        self.assertIsNone(config["param_to_vary_info"])
