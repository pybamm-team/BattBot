import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator


def degradation_parameter_generator(
    chemistry,
    number_of_values,
    degradation_mode=None,
    degradation_value=None
):
    """
    Generates a random degradation parameter and random values for the same.
    Parameters:
        chemistry: dict
        number_of_values: numerical
        degradation_mode: str
        degradation_value: str
    Returns:
        param_values: list
        degradation_parameter: str
    """

    if chemistry == pybamm.parameter_sets.Ai2020:
        if (
            degradation_mode == "particle mechanics"
            and degradation_value == "swelling and cracking"
        ):
            degradation_parameters = [
                "Negative electrode Paris' law constant b",
                "Positive electrode Paris' law constant b",
                "Negative electrode Paris' law constant m",
                "Positive electrode Paris' law constant m",
                "Negative electrode Poisson's ratio",
                "Positive electrode Poisson's ratio",
                "Negative electrode Young's modulus [Pa]",
                "Positive electrode Young's modulus [Pa]",
                "Negative electrode initial crack length [m]",
                "Positive electrode initial crack length [m]",
                "Negative electrode initial crack width [m]",
                "Positive electrode initial crack width [m]",
                "Negative electrode reference concentration for free of deformation [mol.m-3]", # noqa
                "Positive electrode reference concentration for free of deformation [mol.m-3]"  # noqa
            ]

    elif (
        chemistry == pybamm.parameter_sets.Chen2020
        or chemistry == pybamm.parameter_sets.Marquis2019
    ):
        if degradation_mode == "SEI":
            degradation_parameters = []
            if degradation_value == "ec reaction limited":
                degradation_parameters = [
                    "EC initial concentration in electrolyte [mol.m-3]",
                    "SEI open-circuit potential [V]",
                ]
            elif degradation_value == "solvent-diffusion limited":
                degradation_parameters = [
                    "Bulk solvent concentration [mol.m-3]"
                ]
            elif degradation_value == "electron-migration limited":
                degradation_parameters = [
                    "Inner SEI open-circuit potential [V]"
                ]
            elif degradation_value == "interstitial-diffusion limited":
                degradation_parameters = [
                    "Lithium interstitial reference concentration [mol.m-3]"
                ]

            degradation_parameters.append("Ambient temperature [K]")

    degradation_parameter = random.choice(degradation_parameters)

    param_values = []
    for i in range(0, number_of_values):
        param_values.append(
            parameter_value_generator(chemistry, degradation_parameter)
        )

    return param_values, degradation_parameter
