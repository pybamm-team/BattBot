import os
import unittest

import pybamm
from bot.plotting.comparison_generator import ComparisonGenerator


class TestComparisonGenerator(unittest.TestCase):
    def setUp(self):
        self.model_for_comp = {"DFN": pybamm.lithium_ion.DFN()}
        self.models_for_comp = {
            "DFN": pybamm.lithium_ion.DFN(),
            "SPM": pybamm.lithium_ion.SPM(),
        }
        self.chemistry = "Chen2020"
        self.params = pybamm.ParameterValues(self.chemistry)
        self.cycle = [
            (
                "Discharge at C/10 for 10 hours or until 3.3 V",
                "Rest for 1 hour",
                "Charge at 1 A until 4.1 V",
                "Hold at 4.1 V until 50 mA",
                "Rest for 1 hour",
            )
        ]
        self.number = 1
        self.is_experiment = False
        self.param_to_vary_info = {
            "Current function [A]": {"print_name": None, "bounds": (None, None)}
        }

    def tearDown(self):
        os.remove("plot.gif")

    def test_comparsion_generator(self):
        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary_info=self.param_to_vary_info,
            params=self.params,
        )

        comparison_generator.parameter_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], list)
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary_info=self.param_to_vary_info,
            params=self.params,
            varied_values_override=[5.2, 5.4, 5.6],
        )

        comparison_generator.parameter_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], list)
        assert isinstance(comparison_generator.comparison_dict["params"], dict)
        assert (
            comparison_generator.comparison_dict["params"][0]["Current function [A]"]
            == 5.2
        )
        assert (
            comparison_generator.comparison_dict["params"][1]["Current function [A]"]
            == 5.4
        )
        assert (
            comparison_generator.comparison_dict["params"][2]["Current function [A]"]
            == 5.6
        )

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            params=self.params,
        )

        comparison_generator.model_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], dict)
        assert (
            "Current function [A]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert (
            "Ambient temperature [K]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert len(comparison_generator.comparison_dict["varied_values"]) == 2
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        self.is_experiment = True
        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            param_to_vary_info=self.param_to_vary_info,
            params=self.params,
        )

        comparison_generator.parameter_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], list)
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry="Ai2020",
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            param_to_vary_info=self.param_to_vary_info,
            params=pybamm.ParameterValues("Ai2020"),
        )

        comparison_generator.parameter_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], list)
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry="Ai2020",
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            params=pybamm.ParameterValues("Ai2020"),
        )

        comparison_generator.model_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], dict)
        assert (
            "Current function [A]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert (
            "Ambient temperature [K]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert len(comparison_generator.comparison_dict["varied_values"]) == 2
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            params=self.params,
        )

        comparison_generator.model_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], dict)
        assert (
            "Current function [A]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert (
            "Ambient temperature [K]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert len(comparison_generator.comparison_dict["varied_values"]) == 2
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.models_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            cycle=self.cycle,
            number=self.number,
            params=self.params,
        )

        comparison_generator.model_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], dict)
        assert (
            "Current function [A]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert (
            "Ambient temperature [K]"
            in comparison_generator.comparison_dict["varied_values"]
        )
        assert len(comparison_generator.comparison_dict["varied_values"]) == 2
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        self.is_experiment = False

        comparison_generator = ComparisonGenerator(
            models_for_comp=self.model_for_comp,
            chemistry=self.chemistry,
            is_experiment=self.is_experiment,
            param_to_vary_info={
                "Negative electrode exchange-current density [A.m-2]": {
                    "print_name": r"$j_{0,n}$",
                    "bounds": (None, None),
                }
            },
            params=self.params,
        )

        comparison_generator.parameter_comparison(testing=True)

        assert isinstance(comparison_generator.comparison_dict["varied_values"], list)
        assert isinstance(comparison_generator.comparison_dict["params"], dict)

        assert os.path.exists("plot.gif")


if __name__ == "__main__":
    unittest.main()
