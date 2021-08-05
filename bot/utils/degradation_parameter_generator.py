import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator


def degradation_parameter_generator(
    chemistry, number_of_comp, degradation_mode=None, degradation_value=None
):
    """
    Generates a random degradation parameter and random values for the same.
    Parameters:
        chemistry: dict
        number_of_comp: numerical
        degradation_mode: str
        degradation_value: str
    Returns:
        param_values: list
        degradation_parameter: str
    """

    params = pybamm.ParameterValues(chemistry=chemistry)
    if chemistry == pybamm.parameter_sets.Ai2020:
        print("yes")
        if (
            degradation_mode == "particle mechanics"
            and degradation_value == "swelling and cracking"
        ):
            degradation_parameters = {
                "Negative electrode Paris' law constant b": (None, None),
                "Positive electrode Paris' law constant b": (None, None),
                "Negative electrode Paris' law constant m": (None, None),
                "Positive electrode Paris' law constant m": (None, None),
                "Negative electrode Poisson's ratio": (None, None),
                "Positive electrode Poisson's ratio": (None, None),
                "Negative electrode Young's modulus [Pa]": (None, None),
                "Positive electrode Young's modulus [Pa]": (None, None),
                "Negative electrode reference concentration for free of deformation [mol.m-3]": (  # noqa
                    None,
                    None,
                ),
                "Positive electrode reference concentration for free of deformation [mol.m-3]": (  # noqa
                    None,
                    None,
                ),
            }

    elif (
        chemistry == pybamm.parameter_sets.Chen2020
        or chemistry == pybamm.parameter_sets.Marquis2019
    ):
        if degradation_mode == "SEI":
            degradation_parameters = {}
            if degradation_value == "ec reaction limited":
                degradation_parameters.update(
                    {
                        "EC initial concentration in electrolyte [mol.m-3]": (
                            None,
                            None,
                        ),
                        "SEI open-circuit potential [V]": (None, None),
                    }
                )
            elif degradation_value == "solvent-diffusion limited":
                degradation_parameters.update(
                    {"Bulk solvent concentration [mol.m-3]": (None, None)}
                )
            elif degradation_value == "electron-migration limited":
                degradation_parameters.update(
                    {"Inner SEI open-circuit potential [V]": (None, None)}
                )
            elif degradation_value == "interstitial-diffusion limited":
                degradation_parameters.update(
                    {
                        "Lithium interstitial reference concentration [mol.m-3]": (
                            None,
                            None,
                        )
                    }
                )

            degradation_parameters.update({"Ambient temperature [K]": (265, 355)})

    degradation_parameter = random.choice(list(degradation_parameters.keys()))

    param_values = []
    for i in range(0, number_of_comp):
        params = parameter_value_generator(
            params.copy(),
            {degradation_parameter: degradation_parameters[degradation_parameter]},
        )
        param_values.append(params)

    return param_values, degradation_parameter
