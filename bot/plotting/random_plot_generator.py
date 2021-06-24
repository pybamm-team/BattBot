import pybamm
import random
import logging
from plotting.plot_graph import plot_graph
from models.model_solver import model_solver
from utils.parameter_value_generator import parameter_value_generator
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

# possible "SEI porosity change" for the bot
sei_porosity_change_list = ["true", "false"]

# possible "lithium plating" for the bot
lithium_plating_list = ["reversible", "irreversible"]

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
            choice: numerical
                default: None
                Should be used only during testing, using this one can test
                different parts of this function deterministically without
                relying on the random functions to execute that part.
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
            sei_porosity_change = random.choice(sei_porosity_change_list)
            lithium_plating = random.choice(lithium_plating_list)

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

            # randomly choose a plot if not testing
            # 0: pre-defined model with a pre-defined chemistry
            # 1: experiment or comparison with summary variable
            # 2: experiment without summary variables
            # 3: comparison plots
            if options["choice"] is None:
                options["choice"] = random.randint(0, 3)

            # Add degradation only if we are plotting summary variables
            if options["choice"] == 1:
                # update model options
                model_options = {}
                if options["chemistry"] == (
                    pybamm.parameter_sets.Ai2020
                ):
                    model_options.update({
                        "particle mechanics": particle_mechanics,
                    })
                elif options["chemistry"] == (
                    pybamm.parameter_sets.Yang2017
                ):
                    model_options.update({
                        "lithium plating": "irreversible",
                    })
                elif options["chemistry"] == (
                    pybamm.parameter_sets.Chen2020_plating
                ):
                    options.update({
                        "lithium plating": lithium_plating,
                        "SEI porosity change": sei_porosity_change
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

            # vary the lower voltage
            lower_voltage = parameter_value_generator(
                options["chemistry"], "Lower voltage cut-off [V]"
            )

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

            if options["choice"] == 0:

                # taking a random Crate and all the random configurations
                # selected above
                c_rate = random.randint(0, 3)

                # solving
                (parameter_values, sim, solution) = model_solver(
                    model=model,
                    chemistry=options["chemistry"],
                    solver=solver,
                    c_rate=c_rate,
                    lower_voltage=lower_voltage,
                )

                # creating the GIF
                time_array = plot_graph(solution, sim)

                return_dict.update({
                    "model": model,
                    "parameter_values": parameter_values,
                    "time_array": time_array,
                    "chemistry": options["chemistry"],
                    "solver": solver.name,
                    "is_experiment": False,
                    "cycle": None,
                    "number": None,
                    "is_comparison": False
                })

                return

            elif options["choice"] == 1:

                # generating number of comparisons
                number_of_comp = random.randint(1, 3)

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
                    solutions,
                    parameter_values
                ) = experiment_solver(
                    model=model,
                    experiment=experiment,
                    chemistry=options["chemistry"],
                    solver=solver,
                    number_of_comp=1
                )

                # plotting summary variables
                generate_summary_variables(solutions, options["chemistry"])

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

            elif options["choice"] == 2:

                # generating a random experiment
                cycle_received = experiment_generator()
                number = random.randint(1, 3)

                experiment = pybamm.Experiment(cycle_received * number)

                # solving
                (sim, solutions, parameter_values) = experiment_solver(
                    model, experiment, options["chemistry"], solver, 1
                )

                # creating a GIF
                time_array = plot_graph(solutions[0], sim)

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

            elif options["choice"] == 3:

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
