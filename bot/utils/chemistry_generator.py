import pybamm
from utils.single_point_decimal import single_decimal_point


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
            param_value = single_decimal_point(2.5, 4.0, 1)

        elif chemistry == pybamm.parameter_sets.Marquis2019:
            param_value = single_decimal_point(3.1, 3.9, 1)

        elif chemistry == pybamm.parameter_sets.Ai2020:
            param_value = single_decimal_point(2.7, 3.9, 1)

        elif chemistry == pybamm.parameter_sets.Yang2017:
            param_value = single_decimal_point(2.7, 3.9, 1)

    elif parameter == "Current function [A]":
        if chemistry == pybamm.parameter_sets.Chen2020:
            param_value = single_decimal_point(3, 5, 2)

        elif chemistry == pybamm.parameter_sets.Marquis2019:
            param_value = single_decimal_point(0.1, 0.7, 2)

        elif chemistry == pybamm.parameter_sets.Ai2020:
            param_value = single_decimal_point(0.5, 2.25, 2)

        elif chemistry == pybamm.parameter_sets.Yang2017:
            param_value = single_decimal_point(0.5, 2.25, 2)

    return param_value
