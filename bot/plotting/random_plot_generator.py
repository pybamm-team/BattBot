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
        testing: bool
            default: None
        provided_choice: numerical
            default: None
        provided_degradation: bool
            default: True
        provided_chemistry: dict
            default: None
    """

    while True:

        try:
            pybamm.set_logging_level("NOTICE")
            chemistries = [
                pybamm.parameter_sets.Ai2020,
                pybamm.parameter_sets.Chen2020,
                pybamm.parameter_sets.Marquis2019,
                pybamm.parameter_sets.Yang2017,
                # pybamm.parameter_sets.Ecker2015,
                # pybamm.parameter_sets.Ramadass2004,
            ]

            chemistry = random.choice(chemistries)

            if provided_chemistry is not None:
                chemistry = provided_chemistry

            particle_mechanics_list = [
                "swelling and cracking",
                "swelling only",
                "none"
            ]
            sei_list = [
                "ec reaction limited",
                "reaction limited",
                "solvent-diffusion limited",
                "electron-migration limited",
                "interstitial-diffusion limited",
                "none"
            ]
            options = {}

            particle_mechanics = random.choice(particle_mechanics_list)
            sei = random.choice(sei_list)

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

            if chemistry == pybamm.parameter_sets.Ai2020:
                options.update({
                    "particle mechanics": particle_mechanics,
                    "SEI": sei
                })
            elif chemistry == pybamm.parameter_sets.Yang2017:
                options.update({
                    "lithium plating": "irreversible",
                    "lithium plating porosity change": "true",
                    "SEI": "ec reaction limited"
                })
            elif chemistry != pybamm.parameter_sets.Yang2017:
                options.update({
                    "SEI": sei,
                })

            solvers = [
                pybamm.CasadiSolver(mode="safe"),
                pybamm.CasadiSolver(mode="fast with events")
            ]

            solver = random.choice(solvers)

            choice = random.randint(0, 3)

            if testing is True and provided_choice is not None:
                choice = provided_choice

            if choice == 1:
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
            else:
                models = [
                    pybamm.lithium_ion.DFN(),
                    pybamm.lithium_ion.SPM(),
                    pybamm.lithium_ion.SPMe()
                ]

            model = random.choice(models)

            lower_voltage = parameter_value_generator(
                chemistry, "Lower voltage cut-off [V]"
            )

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

                c_rate = random.randint(0, 3)
                (parameter_values, sim, solution) = model_solver(
                    model=model,
                    chemistry=chemistry,
                    solver=solver,
                    c_rate=c_rate,
                    lower_voltage=lower_voltage,
                )

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
                cycle_received = experiment_generator()
                number = random.randint(4, 100)

                experiment = pybamm.Experiment(
                    cycle_received * number, termination="80% capacity"
                )
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

                generate_summary_variables(solution)

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

                cycle_received = experiment_generator()
                number = random.randint(1, 3)

                experiment = pybamm.Experiment(cycle_received * number)
                (sim, solution, parameter_values) = experiment_solver(
                    model, experiment, chemistry, solver
                )

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

                number_of_comp = random.randint(1, 3)
                if testing:
                    number_of_comp = 1
                random.shuffle(models)
                models_for_comp = models[:number_of_comp]
                models_for_comp = dict(list(enumerate(models_for_comp)))

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
