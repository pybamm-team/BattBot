import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator


def degradation_parameter_generator(
    chemistry, number_of_comp, degradation_mode, degradation_value
):
    """
    Generates a random degradation parameter and random values for the same.
    Parameters:
        chemistry: dict
        number_of_comp: numerical
            Number of times a parameter has to be varied.
        degradation_mode: str
            The degradation option added to a model. Can be "SEI" and
            "particle mechanics".
        degradation_value: str
            Value of the degradation mode.
    Returns:
        param_values: list
        degradation_parameter: str
    """

    params = pybamm.ParameterValues(chemistry=chemistry)
    if degradation_mode == "particle mechanics":
        degradation_parameters = {
            "Negative electrode Paris' law constant b": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Positive electrode Paris' law constant b": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Negative electrode Paris' law constant m": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Positive electrode Paris' law constant m": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Negative electrode Poisson's ratio": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Positive electrode Poisson's ratio": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Negative electrode Young's modulus [Pa]": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Positive electrode Young's modulus [Pa]": {
                "print_name": None,
                "bounds": (None, None),
            },
            "Negative electrode reference concentration for free of deformation [mol.m-3]": {  # noqa
                "print_name": None,
                "bounds": (None, None),
            },
            "Positive electrode reference concentration for free of deformation [mol.m-3]": {  # noqa
                "print_name": None,
                "bounds": (None, None),
            },
        }

    if degradation_mode == "SEI":
        degradation_parameters = {}
        if degradation_value == "ec reaction limited":
            degradation_parameters.update(
                {
                    "EC initial concentration in electrolyte [mol.m-3]": {
                        "print_name": None,
                        "bounds": (None, None),
                    },
                    "SEI open-circuit potential [V]": {
                        "print_name": None,
                        "bounds": (None, None),
                    },
                }
            )
        elif degradation_value == "solvent-diffusion limited":
            degradation_parameters.update(
                {
                    "Bulk solvent concentration [mol.m-3]": {
                        "print_name": None,
                        "bounds": (None, None),
                    }
                },
            )
        elif degradation_value == "electron-migration limited":
            degradation_parameters.update(
                {
                    "Inner SEI open-circuit potential [V]": {
                        "print_name": None,
                        "bounds": (None, None),
                    },
                }
            )
        elif degradation_value == "interstitial-diffusion limited":
            degradation_parameters.update(
                {
                    "Lithium interstitial reference concentration [mol.m-3]": {
                        "print_name": None,
                        "bounds": (None, None),
                    },
                }
            )

        degradation_parameters.update(
            {
                "Ambient temperature [K]": {"print_name": None, "bounds": (265, 355)},
            }
        )

    degradation_parameter = random.choice(list(degradation_parameters.keys()))

    param_values = []
    for i in range(0, number_of_comp):
        params = parameter_value_generator(
            params.copy(),
            {
                degradation_parameter: degradation_parameters[degradation_parameter][
                    "bounds"
                ]
            },
        )
        param_values.append(params)

    return param_values, degradation_parameter
