import random
import pybamm
from utils.single_point_decimal import single_decimal_point


def chemistry_generator(chemistry_name):

    if chemistry_name == pybamm.parameter_sets.Chen2020:
        lower_voltage = single_decimal_point(2.5, 4.0, 0.1)
        ambient_temp = random.uniform(273.18, 298.15)
        initial_temp = random.uniform(273.18, 298.15)
        reference_temp = random.uniform(273.18, 298.15)

    elif chemistry_name == pybamm.parameter_sets.Marquis2019:
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
