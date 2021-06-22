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


def random_plot_generator(
    return_dict,
    testing=False,
    provided_choice=None,
    provided_chemistry=None,
    provided_degradation=True,
):
    """
    Generates a random plot.
    Parameters:
        return_dict: dict
            A shared dictionary in which all the return values are stored.
        testing: bool
            default: False
            Should be set to True when testing, this helps the tests to
            execute small chunks of this function deterministically.
        provided_choice: numerical
            default: None
            Should be used only during testing, using this one can test
            different parts of this function deterministically without relying
            on the random functions to execute that part.
        provided_chemistry: dict
            default: None
            Should be used only during testing, using this one can test
            different parts of this function deterministically without relying
            on the random functions to execute that part.
        provided_degradation: bool
            default: True
            Using this one can test and cover some probabilistic lines where
            no degradation option of a model is selected.
    """

    while True:

        try:
            pybamm.set_logging_level("NOTICE")

            chemistries = [
                pybamm.parameter_sets.Ai2020,
                pybamm.parameter_sets.Chen2020,
                pybamm.parameter_sets.Marquis2019,
                pybamm.parameter_sets.Yang2017,
                pybamm.parameter_sets.Chen2020_plating,
                # pybamm.parameter_sets.Ecker2015,
                # pybamm.parameter_sets.Ramadass2004,
            ]

            # choosing a random chemistry
            chemistry = random.choice(chemistries)

            # don't randomly select a chemistry if testing
            if provided_chemistry is not None:
                chemistry = provided_chemistry

            particle_mechanics_list = [
                "swelling and cracking",
                # "none"
            ]
            sei_list = [
                "ec reaction limited",
                "reaction limited",
                "solvent-diffusion limited",
                "electron-migration limited",
                "interstitial-diffusion limited",
                # "none"
            ]
            sei_porosity_change_list = ["true", "false"]
            lithium_plating_list = ["reversible", "irreversible"]
            options = {}

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
                    testing
                    and provided_degradation
                )
            ):
                provided_degradation = False
                continue

            # update model options
            if chemistry == pybamm.parameter_sets.Ai2020:
                options.update({
                    "particle mechanics": particle_mechanics,
                })
            elif chemistry == pybamm.parameter_sets.Yang2017:
                options.update({
                    "lithium plating": "irreversible",
                })
            elif chemistry == pybamm.parameter_sets.Chen2020_plating:
                options.update({
                    "lithium plating": lithium_plating,
                    "SEI porosity change": sei_porosity_change
                })
            else:
                options.update({
                    "SEI": sei,
                    "SEI porosity change": sei_porosity_change
                })

            solvers = [
                pybamm.CasadiSolver(mode="safe"),
                pybamm.CasadiSolver(mode="fast with events")
            ]

            # choose a random solver
            solver = random.choice(solvers)

            # 0: pre-defined model with a pre-defined chemistry
            # 1: experiment with summary variable
            # 2: experiment without summary variables
            # 3: comparison plots
            choice = random.randint(0, 3)

            # if testing, don't randomly choose stuff
            if testing is True and provided_choice is not None:
                choice = provided_choice

            # Add degradation only if we are plotting summary variables
            if choice != 1:
                options = None

            models = [
                pybamm.lithium_ion.DFN(
                    options=options
                ),
                pybamm.lithium_ion.SPM(
                    options=options
                ),
                pybamm.lithium_ion.SPMe(
                    options=options
                ),
            ]

            # choose a random model
            model = random.choice(models)

            # vary the lower voltage
            lower_voltage = parameter_value_generator(
                chemistry, "Lower voltage cut-off [V]"
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
                + str(chemistry["citation"])
            )

            if choice == 0:

                # taking a random Crate and all the random configurations
                # selected above
                c_rate = random.randint(0, 3)

                # solving
                (parameter_values, sim, solution) = model_solver(
                    model=model,
                    chemistry=chemistry,
                    solver=solver,
                    c_rate=c_rate,
                    lower_voltage=lower_voltage,
                )

                # creating the GIF
                time_array = plot_graph(solution, sim)

                return_dict["model"] = model
                return_dict["parameter_values"] = parameter_values
                return_dict["time_array"] = time_array
                return_dict["chemistry"] = chemistry
                return_dict["solver"] = solver.name
                return_dict["is_experiment"] = False
                return_dict["cycle"] = None
                return_dict["number"] = None
                return_dict["is_comparison"] = False

                return

            elif choice == 1:

                # generating a random experiment
                cycle_received = experiment_generator()
                number = random.randint(4, 100)

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
                    chemistry=chemistry,
                    solver=solver
                )

                generate_summary_variables([solution])

                return_dict["model"] = model
                return_dict["parameter_values"] = parameter_values
                return_dict["time_array"] = None
                return_dict["chemistry"] = chemistry
                return_dict["solver"] = solver.name
                return_dict["is_experiment"] = True
                return_dict["cycle"] = cycle_received
                return_dict["number"] = number
                return_dict["is_comparison"] = False

                return

            elif choice == 2:

                # generating a random experiment
                cycle_received = experiment_generator()
                number = random.randint(1, 3)

                experiment = pybamm.Experiment(cycle_received * number)

                # solving
                (sim, solution, parameter_values) = experiment_solver(
                    model, experiment, chemistry, solver
                )

                # creating a GIF
                time_array = plot_graph(solution, sim)

                return_dict["model"] = model
                return_dict["parameter_values"] = parameter_values
                return_dict["time_array"] = None
                return_dict["chemistry"] = chemistry
                return_dict["solver"] = solver.name
                return_dict["is_experiment"] = True
                return_dict["cycle"] = cycle_received
                return_dict["number"] = number
                return_dict["is_comparison"] = False

                return

            elif choice == 3:

                # generating number of models to be compared
                number_of_comp = random.randint(1, 3)

                # don't select randomly if testing
                if testing:
                    number_of_comp = 1

                # selecting the models for comparison
                random.shuffle(models)
                models_for_comp = models[:number_of_comp]
                models_for_comp = dict(list(enumerate(models_for_comp)))

                # generating a comparison GIF
                comparison_dict = comparison_generator(
                    number_of_comp,
                    models_for_comp,
                    chemistry,
                )

                return_dict["model"] = comparison_dict["model"]
                return_dict["parameter_values"] = (
                    comparison_dict["parameter_values"]
                )
                return_dict["time_array"] = comparison_dict["time_array"]
                return_dict["chemistry"] = comparison_dict["chemistry"]
                return_dict["solver"] = None
                return_dict["is_experiment"] = False
                return_dict["cycle"] = None
                return_dict["number"] = None
                return_dict["is_comparison"] = True

                return

        except Exception as e:  # pragma: no cover
            print(e)
