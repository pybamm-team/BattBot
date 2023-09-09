import unittest

import pybamm
from bot.utils.degradation_parameter_generator import (
    degradation_parameter_generator,
    graphite_volume_change_Ai2020,
    lico2_volume_change_Ai2020,
)


class TestDegradationParameterGenerator(unittest.TestCase):
    def test_degradation_parameter_generator(self):
        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Ai2020",
            2,
            degradation_mode="particle mechanics",
            degradation_value="swelling and cracking",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Chen2020",
            2,
            degradation_mode="SEI",
            degradation_value="reaction limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Chen2020",
            2,
            degradation_mode="SEI",
            degradation_value="ec reaction limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Chen2020",
            2,
            degradation_mode="SEI",
            degradation_value="solvent-diffusion limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Chen2020",
            2,
            degradation_mode="SEI",
            degradation_value="electron-migration limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Chen2020",
            2,
            degradation_mode="SEI",
            degradation_value="interstitial-diffusion limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Mohtat2020",
            2,
            degradation_mode="SEI",
            degradation_value="interstitial-diffusion limited",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        (param_values, degradation_parameter) = degradation_parameter_generator(
            "Mohtat2020",
            2,
            degradation_mode="particle mechanics",
            degradation_value="swelling only",
        )
        assert isinstance(param_values, list)
        assert isinstance(param_values[0], pybamm.ParameterValues)
        assert len(param_values) == 2
        assert isinstance(degradation_parameter, str)

        t_change = lico2_volume_change_Ai2020(5, 3)
        assert isinstance(
            t_change, pybamm.expression_tree.binary_operators.Multiplication
        )
        t_change = graphite_volume_change_Ai2020(5, 1)
        assert t_change == 103545409.4049503


if __name__ == "__main__":
    unittest.main()
