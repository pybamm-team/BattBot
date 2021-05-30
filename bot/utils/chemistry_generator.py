import random
import pybamm
from utils.single_point_decimal import single_decimal_point


def chemistry_generator(chemistry):
    """
    Generates random values for "Lower voltage cut-off [V]",
    "Ambient temperature [K]", "Initial temperature [K]" and
    "Reference temperature [K]" for a given chemistry.
    Parameters:
        chemistry: dict
    Returns:
        lower_voltage: numerical
        ambient_temp: numerical
        initial_temp: numerical
        reference_temp: numerical
    """

    if chemistry == pybamm.parameter_sets.Chen2020:
        lower_voltage = single_decimal_point(2.5, 4.0, 0.1)
        ambient_temp = random.uniform(273.18, 298.15)
        initial_temp = random.uniform(273.18, 298.15)
        reference_temp = random.uniform(273.18, 298.15)

    elif chemistry == pybamm.parameter_sets.Marquis2019:
        lower_voltage = single_decimal_point(3.1, 3.9, 0.1)
        ambient_temp = random.uniform(273.18, 298.15)
        initial_temp = random.uniform(273.18, 298.15)
        reference_temp = random.uniform(273.18, 298.15)

    return (
        lower_voltage,
        ambient_temp,
        initial_temp,
        reference_temp,
    )
