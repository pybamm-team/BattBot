import pybamm
from utils.desired_decimal_point_generator import (
    desired_decimal_point_generator
)


# implementation by @tinosulzer
class FunctionLike:
    "Behaves like a function but saves fun and parameter"

    def __init__(self, fun, parameter):
        self.fun = fun
        self.parameter = parameter


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
    params = pybamm.ParameterValues(chemistry=chemistry)
    base_value = {}

    if callable(params[parameter]):
        base_value[parameter] = 1.0
        params[parameter] = FunctionLike(params[parameter], parameter)
    else:
        base_value[parameter] = params[parameter]
        params[parameter] = pybamm.InputParameter(parameter)

    param_value = desired_decimal_point_generator(
        base_value[parameter]*0.9, base_value[parameter]*1.1, 2
    )

    return param_value
