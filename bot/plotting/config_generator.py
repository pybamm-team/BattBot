import random
import pybamm
from experiment.experiment_generator import experiment_generator

# possible chemistries for the bot
chemistries = [
    pybamm.parameter_sets.Ai2020,
    pybamm.parameter_sets.Chen2020,
    pybamm.parameter_sets.Marquis2019,
    pybamm.parameter_sets.Yang2017,
    # pybamm.parameter_sets.Ecker2015,
    # pybamm.parameter_sets.Ramadass2004,
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
# parameter: ("lower_bound", "upper_bound")
# if the bounds are given as None, the default bounds will be used -
# parameter: (parameter_values[parameter] / 2, parameter_values[parameter] * 2)
# the varied value will always be in these bounds
param_to_vary_dict = {
    "Current function [A]": (None, None),
    "Electrode height [m]": (0.1, None),
    "Electrode width [m]": (0.1, None),
    "Negative electrode conductivity [S.m-1]": (None, None),
    "Negative electrode porosity": (None, None),
    "Negative electrode active material volume fraction": (None, None),
    "Negative electrode Bruggeman coefficient (electrolyte)": (None, None),
    "Negative electrode exchange-current density [A.m-2]": (None, None),
    "Positive electrode porosity": (None, None),
    "Positive electrode exchange-current density [A.m-2]": (None, None),
    "Positive electrode Bruggeman coefficient (electrolyte)": (None, None),
    "Ambient temperature [K]": (265, 355),
}


def config_generator(choice, test_config=None):
    """
    Generates a random configuration to plot.
    Parameters:
        choice: str
        test_config: dict
            Should be used while testing to deterministically test this
            function.
    Returns:
        config: dict
    """
    config = {}
    model_options = {}

    chemistry = random.choice(chemistries)

    if choice == "degradation comparison (summary variables)":
        if chemistry == pybamm.parameter_sets.Ai2020:
            particle_mechanics = random.choice(particle_mechanics_list)
            model_options.update({
                "particle mechanics": particle_mechanics,
            })
        elif chemistry == pybamm.parameter_sets.Yang2017:
            model_options.update({
                "lithium plating": "irreversible",
                "lithium plating porosity change": "true",
            })
        else:
            sei = random.choice(sei_list)
            model_options.update({
                "SEI": sei,
            })
    elif choice == "non-degradation comparisons":
        model_options = None

    models = [
        pybamm.lithium_ion.DFN(
            options=model_options
        ),
        pybamm.lithium_ion.SPM(
            options=model_options
        ),
        pybamm.lithium_ion.SPMe(
            options=model_options
        ),
    ]

    if choice == "non-degradation comparisons":

        # randomly generating number of models to be compared
        number_of_comp = random.randint(1, 3)

        # selecting the models for comparison
        random.shuffle(models)
        models_for_comp = models[:number_of_comp]
        models_for_comp = dict(list(enumerate(models_for_comp)))

        # if the comparison should be made with an experiment
        is_experiment = random.choice([True, False])

        # generating a random experiment
        if is_experiment:
            cycle = experiment_generator()
            number = random.randint(1, 3)
        else:
            cycle = None
            number = None

        # remove "Current function [A]" from the dict if simulating an
        # experiment and add it back if not an experiment
        # (adding it back because pop edits the original dict)
        if (
            is_experiment
            and "Current function [A]" in param_to_vary_dict
        ):
            param_to_vary_dict.pop("Current function [A]")
        elif (
            not is_experiment
            and "Current function [A]" not in param_to_vary_dict
        ):
            param_to_vary_dict.update({
                "Current function [A]": (None, None)
            })

        if number_of_comp == 1:
            param_to_vary = random.choice(
                list(
                    param_to_vary_dict.keys()
                )
            )
        else:
            param_to_vary = None

        config.update({
            "chemistry": chemistry,
            "number_of_comp": number_of_comp,
            "models_for_comp": models_for_comp,
            "is_experiment": is_experiment,
            "cycle": cycle,
            "number": number,
            "param_to_vary": param_to_vary,
            "param_to_vary_dict": param_to_vary_dict
        })

    elif choice == "degradation comparison (summary variables)":

        model = random.choice(models)

        cycle = experiment_generator()
        number = random.randint(4, 100)

        config.update({
            "model": model,
            "chemistry": chemistry,
            "cycle": cycle,
            "number": number,
        })

    return config
