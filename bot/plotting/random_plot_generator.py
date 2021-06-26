import pybamm
import random
import logging
from experiment.experiment_generator import experiment_generator
from experiment.experiment_solver import experiment_solver
from plotting.summary_variables import generate_summary_variables
from plotting.comparison_generator import comparison_generator


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
    "none"
]

# possible "SEI" for the bot
sei_list = [
    "ec reaction limited",
    "reaction limited",
    "solvent-diffusion limited",
    "electron-migration limited",
    "interstitial-diffusion limited",
    "none"
]

solver = pybamm.CasadiSolver(mode="safe")


def random_plot_generator(
    return_dict,
    options={
        "testing": False,
        "choice": None,
        "chemistry": None,
        "provided_degradation": True,
    },
):
    """
    Generates a random plot.
    Parameters:
        return_dict: dict
            A shared dictionary in which all the return values are stored.
        options: dict
            testing: bool
                default: False
                Should be set to True when testing, this helps the tests to
                execute small chunks of this function deterministically.
            choice: str
                default: None
                Type of comparison that should be plotted.
            chemistry: dict
                default: None
                Should be used only during testing, using this one can test
                different parts of this function deterministically without
                relying on the random functions to execute that part.
            provided_degradation: bool
                default: True
                Using this one can test and cover some probabilistic lines
                where no degradation option of a model is selected.
    """

    while True:

        try:
            pybamm.set_logging_level("NOTICE")

            # randomly select a chemistry if not testing
            if options["chemistry"] is None:
                options["chemistry"] = random.choice(chemistries)

            # choosing random degradation
            particle_mechanics = random.choice(particle_mechanics_list)
            sei = random.choice(sei_list)

            # if no degradation or if testing, continue
            if (
                (
                    particle_mechanics == "none"
                    and sei == "none"
                )
                or (
                    options["testing"]
                    and options["provided_degradation"]
                )
            ):
                options["provided_degradation"] = False
                continue

            # Add degradation only if we are plotting summary variables
            if options["choice"] == 1:
                # update model options
                model_options = {}
                if options["chemistry"] == (
                    pybamm.parameter_sets.Ai2020
                ):
                    model_options.update({
                        "particle mechanics": particle_mechanics,
                        "SEI": sei
                    })
                elif options["chemistry"] == (
                    pybamm.parameter_sets.Yang2017
                ):
                    model_options.update({
                        "lithium plating": "irreversible",
                        "lithium plating porosity change": "true",
                        "SEI": "ec reaction limited"
                    })
                else:
                    model_options.update({
                        "SEI": sei,
                    })
            else:
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

            # choose a random model
            model = random.choice(models)

            # logging the configuration
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.info(
                str(model.name)
                + " "
                + str(solver.name)
                + " "
                + str(model.options)
                + " "
                + str(options["chemistry"]["citation"])
            )

            if options["choice"] == (
                "degradation comparison (summary variables)"
            ):

                # generating a random experiment
                cycle_received = experiment_generator()
                number = random.randint(4, 100)

                if options["chemistry"] == pybamm.parameter_sets.Ai2020:
                    experiment = pybamm.Experiment(
                        cycle_received * number
                    )
                else:
                    experiment = pybamm.Experiment(
                        cycle_received * number, termination="80% capacity"
                    )

                # solving
                (
                    sim,
                    solution,
                    parameter_values
                ) = experiment_solver(
                    model=model,
                    experiment=experiment,
                    chemistry=options["chemistry"],
                    solver=solver
                )

                # plotting summary variables
                generate_summary_variables(solution, options["chemistry"])

                return_dict.update({
                    "model": model,
                    "parameter_values": parameter_values,
                    "time_array": None,
                    "chemistry": options["chemistry"],
                    "solver": solver.name,
                    "is_experiment": True,
                    "cycle": cycle_received,
                    "number": number,
                    "is_comparison": False
                })

                return

            elif options["choice"] == "non-degradation comparisons":

                # generating number of models to be compared
                number_of_comp = random.randint(1, 3)

                # selecting the models for comparison
                random.shuffle(models)
                models_for_comp = models[:number_of_comp]
                models_for_comp = dict(list(enumerate(models_for_comp)))

                # generating a comparison GIF
                comparison_dict = comparison_generator(
                    number_of_comp,
                    models_for_comp,
                    options["chemistry"],
                )

                return_dict.update({
                    "model": comparison_dict["model"],
                    "parameter_values": comparison_dict["parameter_values"],
                    "time_array": comparison_dict["time_array"],
                    "chemistry": comparison_dict["chemistry"],
                    "solver": None,
                    "is_experiment": False,
                    "cycle": None,
                    "number": None,
                    "is_comparison": True
                })

                return

        except Exception as e:  # pragma: no cover
            print(e)
