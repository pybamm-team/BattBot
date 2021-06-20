import pybamm
from utils.desired_decimal_point_generator import (
    desired_decimal_point_generator
)


def chemistry_generator(chemistry, parameter):
    """
    Generates random values for "Lower voltage cut-off [V]"
    for a given chemistry.
    Parameters:
        chemistry: dict
        parameter: str
    Returns:
        param_value: numerical
    """

    if parameter == "Lower voltage cut-off [V]":
        if chemistry == pybamm.parameter_sets.Chen2020:
            param_value = desired_decimal_point_generator(2.5, 4.0, 1)

        elif chemistry == pybamm.parameter_sets.Marquis2019:
            param_value = desired_decimal_point_generator(3.1, 3.9, 1)

        elif chemistry == pybamm.parameter_sets.Ai2020:
            param_value = desired_decimal_point_generator(2.7, 3.9, 1)

        elif chemistry == pybamm.parameter_sets.Yang2017:
            param_value = desired_decimal_point_generator(2.7, 3.9, 1)

        elif chemistry == pybamm.parameter_sets.Chen2020_plating:
            param_value = desired_decimal_point_generator(2.7, 3.9, 1)

    elif parameter == "Current function [A]":
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

    return param_value
