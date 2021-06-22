import pybamm
from utils.desired_decimal_point_generator import (
    desired_decimal_point_generator
)


def parameter_value_generator(chemistry, parameter):
    """
    Generates random values for a given parameter and
    for a given chemistry.
    Parameters:
        chemistry: dict
        parameter: str
    Returns:
        param_value: numerical
    """

    if parameter == "Current function [A]":
        if chemistry == pybamm.parameter_sets.Chen2020:
            param_value = desired_decimal_point_generator(3, 5, 2)

        elif chemistry == pybamm.parameter_sets.Marquis2019:
            param_value = desired_decimal_point_generator(0.1, 0.65, 2)

        elif chemistry == pybamm.parameter_sets.Ai2020:
            param_value = desired_decimal_point_generator(0.5, 2.25, 2)

        elif chemistry == pybamm.parameter_sets.Yang2017:
            param_value = desired_decimal_point_generator(0.5, 2.25, 2)

        elif chemistry == pybamm.parameter_sets.Chen2020_plating:
            param_value = desired_decimal_point_generator(3, 5, 2)

    else:
        params = pybamm.ParameterValues(chemistry=chemistry)
        param_value = desired_decimal_point_generator(
            (params[parameter] - 0.1)*0.9, (params[parameter] + 0.1)*1.1, 2
        )

    return param_value
