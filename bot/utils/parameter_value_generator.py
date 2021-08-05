from utils.desired_decimal_point_generator import (
    desired_decimal_point_generator
)


# implementation by @tinosulzer
class FunctionLike:
    "Behaves like a function but saves fun and parameter"

    def __init__(self, fun, parameter):
        self.fun = fun
        self.parameter = parameter

    def __call__(self, *args):
        return self.parameter * self.fun(*args)

    def __str__(self):
        return str(self.parameter)


def parameter_value_generator(
    params,
    parameter_dict,
):
    """
    Generates random values for given parameters and
    plugs them in params.
    Parameters:
        params: pybamm.ParameterValues
        parameter_dict: dict
            Parameters to be varied. Should be of the form -
            {
                "parameter1": (lower_bound, upper_bound),
                "parameter2": (lower_bound, upper_bound),
            }
            where lower_bound and upper_bound can be either
            numerical or None.
    Returns:
        params: pybamm.ParameterValues
    """

    for parameter, bounds in parameter_dict.items():
        if callable(params[parameter]):
            base_value = 1
            new_parameter_value = desired_decimal_point_generator(
                bounds[0] if bounds[0] is not None else base_value*0.5,
                bounds[1] if bounds[1] is not None else base_value*2,
                2
            )
            params[parameter] = FunctionLike(
                params[parameter], new_parameter_value
            )
        else:
            base_value = params[parameter]
            new_parameter_value = desired_decimal_point_generator(
                bounds[0] if bounds[0] is not None else base_value*0.5,
                bounds[1] if bounds[1] is not None else base_value*2,
                2
            )
            params[parameter] = new_parameter_value

    return params
