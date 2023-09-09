import random

import pybamm

from utils.parameter_value_generator import parameter_value_generator


def lico2_volume_change_Ai2020(sto, c_s_max):
    omega = pybamm.Parameter("Positive electrode partial molar volume [m3.mol-1]")
    t_change = omega * c_s_max * sto
    return t_change


def graphite_volume_change_Ai2020(sto, c_s_max):
    p1 = 145.907
    p2 = -681.229
    p3 = 1334.442
    p4 = -1415.710
    p5 = 873.906
    p6 = -312.528
    p7 = 60.641
    p8 = -5.706
    p9 = 0.386
    p10 = -4.966e-05
    t_change = (
        p1 * sto**9
        + p2 * sto**8
        + p3 * sto**7
        + p4 * sto**6
        + p5 * sto**5
        + p6 * sto**4
        + p7 * sto**3
        + p8 * sto**2
        + p9 * sto
        + p10
    )
    return t_change


def degradation_parameter_generator(
    chemistry, number_of_comp, degradation_mode, degradation_value
):
    """
    Generates a random degradation parameter and random values for the same.

    Parameters
    ----------
        chemistry : dict
        number_of_comp : numerical
            Number of times a parameter has to be varied.
        degradation_mode : str
            The degradation option added to a model. Can be "SEI" and
            "particle mechanics".
        degradation_value : str
            Value of the degradation mode.

    Returns
    -------
        param_values : list
            Parameter values with a parameter varied.
        degradation_parameter : str
            Parameter that has been varied.
    """

    params = pybamm.ParameterValues(chemistry)

    if chemistry == "Mohtat2020":
        params.update(
            {
                # mechanical properties
                "Positive electrode Poisson's ratio": 0.3,
                "Positive electrode Young's modulus [Pa]": 375e9,
                "Positive electrode reference concentration for free of deformation [mol.m-3]": 0,  # noqa: E501
                "Positive electrode partial molar volume [m3.mol-1]": -7.28e-7,
                "Positive electrode volume change": lico2_volume_change_Ai2020,
                "Negative electrode volume change": graphite_volume_change_Ai2020,
                # Loss of active materials (LAM) model
                "Positive electrode LAM constant exponential term": 2,
                "Positive electrode critical stress [Pa]": 375e6,
                # mechanical properties
                "Negative electrode Poisson's ratio": 0.3,
                "Negative electrode Young's modulus [Pa]": 15e9,
                "Negative electrode reference concentration for free of deformation [mol.m-3]": 0,  # noqa: E501
                "Negative electrode partial molar volume [m3.mol-1]": 3.1e-6,
                # Loss of active materials (LAM) model
                "Negative electrode LAM constant exponential term": 2,
                "Negative electrode critical stress [Pa]": 60e6,
                # Other
                "Cell thermal expansion coefficient [m.K-1]": 1.48e-6,
                "SEI kinetic rate constant [m.s-1]": 1e-15,
                "Positive electrode LAM constant proportional term [s-1]": 1e-3 / 3600,
                "Negative electrode LAM constant proportional term [s-1]": 1e-3 / 3600,
                "EC diffusivity [m2.s-1]": 2e-18,
            },
            check_already_exists=False,
        )
    if degradation_mode == "particle mechanics":
        if chemistry == "Ai2020":
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
                "Negative electrode reference concentration for free of deformation [mol.m-3]": {  # noqa: E501
                    "print_name": None,
                    "bounds": (0.0, None),
                },
                "Positive electrode reference concentration for free of deformation [mol.m-3]": {  # noqa: E501
                    "print_name": None,
                    "bounds": (None, None),
                },
            }
        elif chemistry == "Mohtat2020":
            degradation_parameters = {
                "Positive electrode LAM constant proportional term [s-1]": {
                    "print_name": None,
                    "bounds": (None, None),
                },
                "Negative electrode LAM constant proportional term [s-1]": {
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

    # generate parameter values by varying a single parameter
    param_values = []
    for _i in range(number_of_comp):
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
