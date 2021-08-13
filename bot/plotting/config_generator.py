import random
import pybamm
from experiment.experiment_generator import experiment_generator
from utils.parameter_value_generator import parameter_value_generator

# possible chemistries for the bot
chemistries = [
    pybamm.parameter_sets.Ai2020,
    pybamm.parameter_sets.Chen2020,
    pybamm.parameter_sets.Marquis2019,
]

# possible "particle mechanics" for the bot, to be used with Ai2020 parameters
particle_mechanics_list = [
    "swelling and cracking",
]

# possible "SEI" for the bot
sei_list = [
    "ec reaction limited",
    "reaction limited",
    "solvent-diffusion limited",
    "electron-migration limited",
    "interstitial-diffusion limited",
]

# parameters that can be varied in comparisons, of the form -
# parameter: {
#   "print_name": str
#   "bounds": (lower_bound, upper_bound)
# }
# if the bounds are given as None, the default bounds will be used -
# (parameter_values[parameter] / 2, parameter_values[parameter] * 2)
# the varied value will always be in these bounds
param_to_vary_dict = {
    "Electrode height [m]": {"print_name": None, "bounds": (0.1, None)},
    "Electrode width [m]": {"print_name": None, "bounds": (0.1, None)},
    "Negative electrode conductivity [S.m-1]": {
        "print_name": None,
        "bounds": (None, None),
    },
    "Negative electrode porosity": {"print_name": None, "bounds": (None, None)},
    "Negative electrode active material volume fraction": {
        "print_name": None,
        "bounds": (None, None),
    },
    "Negative electrode Bruggeman coefficient (electrolyte)": {
        "print_name": None,
        "bounds": (None, None),
    },
    "Negative electrode exchange-current density [A.m-2]": {
        "print_name": r"$j_{0,n}$",
        "bounds": (None, None),
    },
    "Positive electrode porosity": {"print_name": None, "bounds": (None, None)},
    "Positive electrode exchange-current density [A.m-2]": {
        "print_name": r"$j_{0,p}$",
        "bounds": (None, None),
    },
    "Positive electrode Bruggeman coefficient (electrolyte)": {
        "print_name": None,
        "bounds": (None, None),
    },
}


def config_generator(
    choice,
    test_config={"chemistry": None, "is_experiment": None, "number_of_comp": None},
):
    """
    Generates a random configuration to plot.
    Parameters:
        choice: str
            Can be "model comparison", "parameter comparison" or
            "degradation comparison (summary variables)".
        test_config: dict
            Should be used while testing to deterministically test this
            function.
    Returns:
        config: dict
    """
    config = {}
    model_options = {}

    # choose a random chemistry
    # don't select randomly if testing
    if test_config["chemistry"] is not None:
        chemistry = test_config["chemistry"]
    else:
        chemistry = random.choice(chemistries)
    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    # choose random degradation for a degradation comparison
    if choice == "degradation comparison (summary variables)":

        # add degradation / update model options
        if chemistry == pybamm.parameter_sets.Ai2020:
            particle_mechanics = random.choice(particle_mechanics_list)
            model_options.update(
                {
                    "particle mechanics": particle_mechanics,
                }
            )
        else:
            sei = random.choice(sei_list)
            model_options.update(
                {
                    "SEI": sei,
                }
            )

    # no degradation
    else:
        model_options = None

    # list of all the possible models
    models = [
        pybamm.lithium_ion.DFN(options=model_options),
        pybamm.lithium_ion.SPM(options=model_options),
        pybamm.lithium_ion.SPMe(options=model_options),
    ]

    # choose random configuration for no degradation
    if choice == "model comparison" or choice == "parameter comparison":

        # generating number of models to be compared
        # don't select randomly if testing
        if test_config["number_of_comp"] is not None:
            number_of_comp = test_config["number_of_comp"]
        elif choice == "model comparison":
            number_of_comp = random.randint(2, 3)
        elif choice == "parameter comparison":
            number_of_comp = 1

        # selecting the models for comparison
        random.shuffle(models)
        models_for_comp = models[:number_of_comp]
        models_for_comp = dict(list(enumerate(models_for_comp)))

        # if the comparison should be made with an experiment
        # don't select randomly when testing
        if test_config["is_experiment"] is not None:
            is_experiment = test_config["is_experiment"]
        else:
            is_experiment = random.choice([True, False])

        if is_experiment:
            # generating a random experiment
            cycle = experiment_generator()
            number = random.randint(1, 3)
            # generating parameter values with varied "Ambient temperature [K]"
            params = parameter_value_generator(
                parameter_values.copy(),
                {
                    "Ambient temperature [K]": (265, 355),
                },
            )
        else:
            cycle = None
            number = None
            # generating parameter values with varied "Ambient temperature [K]" and
            # "Current function [A]"
            params = parameter_value_generator(
                parameter_values.copy(),
                {
                    "Current function [A]": (None, None),
                    "Ambient temperature [K]": (265, 355),
                },
            )

        # choosing a parameter to be varied
        if choice == "parameter comparison":
            param_to_vary = random.choice(list(param_to_vary_dict.keys()))
        elif choice == "model comparison":
            param_to_vary = None

        # updating the config dictionary
        config.update(
            {
                "chemistry": chemistry,
                "models_for_comp": models_for_comp,
                "is_experiment": is_experiment,
                "cycle": cycle,
                "number": number,
                "param_to_vary_info": {
                    param_to_vary: {
                        "print_name": param_to_vary_dict[param_to_vary]["print_name"],
                        "bounds": param_to_vary_dict[param_to_vary]["bounds"],
                    }
                }
                if param_to_vary is not None
                else None,
                "params": params,
            }
        )

    elif choice == "degradation comparison (summary variables)":

        # choosing a random model
        model = random.choice(models)

        # choosing a random experiment
        cycle = experiment_generator()
        number = random.randint(4, 100)

        # updating the config dictionary
        config.update(
            {
                "model": model,
                "chemistry": chemistry,
                "cycle": cycle,
                "number": number,
            }
        )

    return config
