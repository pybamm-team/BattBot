import unittest

import pybamm
from bot.plotting.config_generator import config_generator


class TestConfigGenerator(unittest.TestCase):
    def test_config_generator(self):
        config = config_generator("degradation comparison")

        assert isinstance(config, dict)
        assert isinstance(config["model"], pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        assert isinstance(config["degradation_parameter"], str)
        assert isinstance(config["degradation_mode"], str)
        assert isinstance(config["degradation_value"], str)
        assert isinstance(config["varied_values"], list)
        assert isinstance(config["param_values"], list)
        for param in config["param_values"]:
            assert isinstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": "Ai2020",
                "is_experiment": None,
                "number_of_comp": None,
                "degradation_mode": None,
            },
        )

        assert isinstance(config, dict)
        assert isinstance(config["model"], pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        assert isinstance(config["degradation_parameter"], str)
        assert isinstance(config["degradation_mode"], str)
        assert isinstance(config["degradation_value"], str)
        assert isinstance(config["varied_values"], list)
        assert isinstance(config["param_values"], list)
        for param in config["param_values"]:
            assert isinstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": "Mohtat2020",
                "is_experiment": None,
                "number_of_comp": None,
                "degradation_mode": "particle mechanics",
            },
        )

        assert isinstance(config, dict)
        assert isinstance(config["model"], pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        assert isinstance(config["degradation_parameter"], str)
        assert isinstance(config["degradation_mode"], str)
        assert isinstance(config["degradation_value"], str)
        assert isinstance(config["varied_values"], list)
        assert isinstance(config["param_values"], list)
        for param in config["param_values"]:
            assert isinstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": "Mohtat2020",
                "is_experiment": None,
                "number_of_comp": None,
                "degradation_mode": "SEI",
            },
        )

        assert isinstance(config, dict)
        assert isinstance(config["model"], pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        assert isinstance(config["degradation_parameter"], str)
        assert isinstance(config["degradation_mode"], str)
        assert isinstance(config["degradation_value"], str)
        assert isinstance(config["varied_values"], list)
        assert isinstance(config["param_values"], list)
        for param in config["param_values"]:
            assert isinstance(param, pybamm.ParameterValues)

        config = config_generator(
            "degradation comparison",
            test_config={
                "chemistry": "Chen2020",
                "is_experiment": None,
                "number_of_comp": None,
                "degradation_mode": None,
            },
        )

        assert isinstance(config, dict)
        assert isinstance(config["model"], pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        pybamm.Experiment(config["cycle"] * config["number"])
        assert isinstance(config["degradation_parameter"], str)
        assert isinstance(config["degradation_mode"], str)
        assert isinstance(config["degradation_value"], str)
        assert isinstance(config["varied_values"], list)
        assert isinstance(config["param_values"], list)
        for param in config["param_values"]:
            assert isinstance(param, pybamm.ParameterValues)

        config = config_generator("parameter comparison")

        assert isinstance(config, dict)
        assert isinstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            assert isinstance(model, pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["is_experiment"], bool)
        assert isinstance(config["cycle"], list) or config["cycle"] is None
        assert isinstance(config["number"], int) or config["number"] is None
        assert isinstance(config["param_to_vary_info"], dict)
        assert isinstance(config["params"], pybamm.ParameterValues)
        assert config["varied_values_override"] is None

        config = config_generator("model comparison")

        assert isinstance(config, dict)
        assert isinstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            assert isinstance(model, pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["is_experiment"], bool)
        assert isinstance(config["cycle"], list) or config["cycle"] is None
        assert isinstance(config["number"], int) or config["number"] is None
        assert config["param_to_vary_info"] is None
        assert isinstance(config["params"], pybamm.ParameterValues)
        assert config["varied_values_override"] is None

        config = config_generator(
            "parameter comparison",
            test_config={"chemistry": None, "is_experiment": True, "number_of_comp": 1},
        )

        assert isinstance(config, dict)
        assert isinstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            assert isinstance(model, pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["is_experiment"], bool)
        assert config["is_experiment"]
        assert isinstance(config["cycle"], list)
        assert isinstance(config["number"], int)
        assert isinstance(config["param_to_vary_info"], dict)
        assert isinstance(config["params"], pybamm.ParameterValues)
        assert config["varied_values_override"] is None

        config = config_generator(
            "model comparison",
            test_config={
                "chemistry": None,
                "is_experiment": False,
                "number_of_comp": 2,
                "degradation_mode": None,
            },
        )

        assert isinstance(config, dict)
        assert isinstance(config["models_for_comp"], dict)
        for model in config["models_for_comp"].values():
            assert isinstance(model, pybamm.BaseBatteryModel)
        assert isinstance(config["chemistry"], str)
        assert isinstance(config["is_experiment"], bool)
        assert not config["is_experiment"]
        assert config["cycle"] is None
        assert config["number"] is None
        assert config["param_to_vary_info"] is None
        assert isinstance(config["params"], pybamm.ParameterValues)
        assert config["varied_values_override"] is None
