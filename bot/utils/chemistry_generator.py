import pybamm
from utils.single_point_decimal import single_decimal_point


def chemistry_generator(chemistry):
    """
    Generates random values for "Lower voltage cut-off [V]"
    for a given chemistry.
    Parameters:
        chemistry: dict
    Returns:
        lower_voltage: numerical
    """

    if chemistry == pybamm.parameter_sets.Chen2020:
        lower_voltage = single_decimal_point(2.5, 4.0, 0.1)

    elif chemistry == pybamm.parameter_sets.Marquis2019:
        lower_voltage = single_decimal_point(3.1, 3.9, 0.1)

    elif chemistry == pybamm.parameter_sets.Ai2020:
        lower_voltage = single_decimal_point(2.7, 3.9, 0.1)

    elif chemistry == pybamm.parameter_sets.Yang2017:
        lower_voltage = single_decimal_point(2.7, 3.9, 0.1)

    return lower_voltage
