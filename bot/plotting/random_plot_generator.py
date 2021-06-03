import pybamm
import random
from plotting.plot_graph import plot_graph
from models.model_solver import model_solver
from utils.chemistry_generator import chemistry_generator
from utils.single_point_decimal import single_decimal_point
from experiment.experiment_generator import experiment_generator
from experiment.experiment_solver import experiment_solver
from plotting.summary_variables import generate_summary_variables


def random_plot_generator(
    testing=False,
    provided_choice=None,
    provided_number_of_comp=None,
    plot_summary_variables=True
):
    """
    Generates a random plot.
    Parameters:
        testing: bool
            default: None
        provided_choice: numerical
            default: None
        provided_number_of_comp: numerical
            default: None
        plot_summary_variables: bool
            default: True
    Returns:
        model: pybamm.BaseModel or dict
        parameter_values: pybamm.ParameterValues
        time: numerical (seconds) or None
        chemistry: dict
        solver: pybamm.BaseSolver
        is_experiment: bool
        cycle: list
        number: numerical
        is_comparison: bool
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

            if particle_mechanics == "none" and sei == "none":
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

            model = random.choice(models)

            choice = random.randint(0, 2)
            if testing is True and provided_choice is not None:
                choice = provided_choice

            solvers = [
                pybamm.CasadiSolver(mode="safe"),
                pybamm.CasadiSolver(mode="fast"),
                pybamm.CasadiSolver(mode="fast with events")
            ]

            solver = random.choice(solvers)

            if choice == 1:
                solver = pybamm.CasadiSolver(mode="safe")

            lower_voltage = chemistry_generator(chemistry)

            if choice == 0:

                c_rate = random.randint(0, 3)
                (parameter_values, sim, solution) = model_solver(
                    model=model,
                    chemistry=chemistry,
                    solver=solver,
                    c_rate=c_rate,
                    lower_voltage=lower_voltage,
                )

                time = plot_graph(solution, sim)

                return (
                    model,
                    parameter_values,
                    time,
                    chemistry,
                    solver,
                    False,
                    None,
                    None,
                    False,
                )

            elif choice == 1:
                (
                    cycle_received,
                    number,
                ) = experiment_generator()
                if testing:
                    number = 10
                if number > 3 and plot_summary_variables:

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
                    return (
                        model,
                        parameter_values,
                        None,
                        chemistry,
                        solver,
                        True,
                        cycle_received,
                        number,
                        False,
                    )
                if testing:
                    number = 1
                experiment = pybamm.Experiment(cycle_received * number)
                (sim, solution, parameter_values) = experiment_solver(
                    model, experiment, chemistry, solver
                )
                time = plot_graph(solution, sim)
                return (
                    model,
                    parameter_values,
                    time,
                    chemistry,
                    solver,
                    True,
                    cycle_received,
                    number,
                    False,
                )

            elif choice == 2:

                number_of_comp = random.randint(1, 3)
                random.shuffle(models)
                models_for_comp = models[:number_of_comp]
                if testing and provided_number_of_comp == 1:
                    models_for_comp = [pybamm.lithium_ion.DFN()]
                models_for_comp = dict(list(enumerate(models_for_comp)))
                params = pybamm.ParameterValues(chemistry=chemistry)
                parameter_values_for_comp = dict(list(enumerate([params])))

                if (
                    number_of_comp == 1
                    or (
                        testing
                        and provided_number_of_comp == 1
                    )
                ):
                    param_list = []
                    diff_params = random.randint(2, 3)
                    for i in range(0, diff_params):
                        param_list.append(params.copy())
                        param_list[i][
                            "Current function [A]"
                        ] = single_decimal_point(4, 6, 0.1)
                    parameter_values_for_comp = dict(
                        list(enumerate(param_list))
                    )

                s = pybamm.BatchStudy(
                    models=models_for_comp,
                    parameter_values=parameter_values_for_comp,
                    permutations=True,
                )

                s.solve([0, 3700])

                time = plot_graph(sim=s.sims)

                return (
                    models_for_comp,
                    params,
                    time,
                    chemistry,
                    None,
                    False,
                    None,
                    None,
                    True,
                )

        except Exception as e:
            print(e)
