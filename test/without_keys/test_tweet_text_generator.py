import unittest

import pybamm
from bot.utils.tweet_text_generator import tweet_text_generator


class TestTweetTextGenerator(unittest.TestCase):
    def setUp(self):
        self.chemistry = "Chen2020"
        self.params = pybamm.ParameterValues(self.chemistry)
        self.c_rate = (
            self.params["Current function [A]"]
            / self.params["Nominal cell capacity [A.h]"]
        )
        self.temp = self.params["Ambient temperature [K]"] - 273.15
        self.model = pybamm.lithium_ion.DFN()
        self.is_experiment = True
        self.cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        self.number = 3
        self.is_comparison = False
        self.param_to_vary = None
        self.params = dict(list(enumerate([self.params])))
        self.degradation_mode = "SEI"
        self.degradation_value = "reaction limited"

    def test_tweet_text_generator(self):
        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert (
            result
            == f"Plotting {self.model.name} with {self.params[0]['citations'][0]} parameters and {self.degradation_value} {self.degradation_mode} for the following experiment 🔽 https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.is_comparison = True
        self.model = {0: pybamm.lithium_ion.DFN(), 1: pybamm.lithium_ion.SPM()}
        self.degradation_mode = None
        self.degradation_value = None

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment == str(self.cycle) + " * " + str(self.number)
        assert (
            result
            == f"Comparing {self.model[0].name} and {self.model[1].name} with {self.params[0]['citations'][0]} parameters at {self.temp}°C for the following experiment 🔽 https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM(),
            2: pybamm.lithium_ion.SPMe(),
        }

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment == str(self.cycle) + " * " + str(self.number)
        assert (
            result
            == f"Comparing Doyle-Fuller-Newman model, Single Particle Model, and Single Particle Model with electrolyte with {self.params[0]['citations'][0]} parameters at {self.temp}°C for the following experiment 🔽 https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.param_to_vary = "Current function [A]"

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment == str(self.cycle) + " * " + str(self.number)
        assert (
            result
            == f"{self.model[0].name} with {self.params[0]['citations'][0]} parameters varying '{self.param_to_vary}' at {self.temp}°C for the following experiment 🔽 https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.is_experiment = False
        self.param_to_vary = None
        self.model = {0: pybamm.lithium_ion.DFN(), 1: pybamm.lithium_ion.SPM()}

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment is None
        assert (
            result
            == f"Comparing {self.model[0].name} and {self.model[1].name} with {self.params[0]['citations'][0]} parameters for a {self.c_rate} C discharge at {self.temp}°C https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.model = {
            0: pybamm.lithium_ion.DFN(),
            1: pybamm.lithium_ion.SPM(),
            2: pybamm.lithium_ion.SPMe(),
        }

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment is None
        assert (
            result
            == f"Comparing {self.model[0].name}, {self.model[1].name}, and {self.model[2].name} with {self.params[0]['citations'][0]} parameters for a {self.c_rate} C discharge at {self.temp}°C https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.param_to_vary = "Electrode height [m]"

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment is None
        assert (
            result
            == f"{self.model[0].name} with {self.params[0]['citations'][0]} parameters varying '{self.param_to_vary}' for a {self.c_rate} C discharge at {self.temp}°C https://bit.ly/3z5p7q9"  # noqa: E501
        )

        self.param_to_vary = "Positive electrode exchange-current density [A.m-2]"
        self.chemistry = "Chen2020"
        self.is_experiment = True

        result, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        assert experiment == str(self.cycle) + " * " + str(self.number)
        assert (
            result
            == f"Doyle-Fuller-Newman model with {self.params[0]['citations'][0]} parameters varying '{self.param_to_vary}' at {self.temp}°C for the following experiment 🔽 https://bit.ly/3z5p7q9"  # noqa: E501
        )


if __name__ == "__main__":
    unittest.main()
