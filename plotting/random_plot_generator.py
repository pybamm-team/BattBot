import pybamm
import random
import sys
import importlib.util
from plotting.plot_graph import plot_graph
from models.model_generator import model_generator
from utils.chemistry_generator import chemistry_generator
from experiment.experiment_generator import experiment_generator
from experiment.experiment_solver import experiment_solver


def random_plot_generator():

    # while True:

    #     try:

    models = [
        pybamm.lithium_ion.DFN(), pybamm.lithium_ion.SPM(),
        pybamm.lithium_ion.SPMe(), pybamm.lithium_ion.NewmanTobias(),
        pybamm.lithium_ion.Yang2017(), pybamm.lithium_ion.BasicDFN(),
        pybamm.lithium_ion.BasicSPM()
    ]

    modelNum = random.randint(0, len(models) - 1)
    model = models[modelNum]
    model = models[0]
    print(model)

    chemistries = [
        pybamm.parameter_sets.Chen2020,
        pybamm.parameter_sets.Marquis2019,
    ]

    chemNum = random.randint(0, len(chemistries) - 1)
    chemistry = chemistries[chemNum]
    chemistry = chemistries[0]
    print(chemistry)

    solvers = [
        pybamm.CasadiSolver(mode="fast"),
        pybamm.CasadiSolver(mode="fast with events"),
    ]

    solverNum = random.randint(0, len(solvers) - 1)
    solver = solvers[solverNum]
    solver = solvers[0]
    print(solver)

    (
        current_function,
        upper_voltage,
        lower_voltage,
        ambient_temp,
        initial_temp,
        reference_temp,
    ) = chemistry_generator(chemistry)

    choice = random.randint(0, 1)
    choice = 0

    if choice == 0:

        if lower_voltage < upper_voltage:
            (parameter_values, sim, solution) = model_generator(
                model=model,
                solver=solver,
                chemistry=chemistry,
                current_function=current_function,
                upper_voltage=upper_voltage,
                lower_voltage=lower_voltage,
                ambient_temp=ambient_temp,
                initial_temp=initial_temp,
                reference_temp=reference_temp,
            )

            time = plot_graph(solution, sim)

            return model, parameter_values, time, chemistry

    elif choice == 1:
        (
            cycleReceived,
            number,
        ) = experiment_generator()
        experiment = pybamm.Experiment(cycleReceived)
        (
            sim, 
            solution
        ) = experiment_solver(model, experiment, chemistry, solver)
        time = plot_graph(solution, sim)
        return (
            parameter_values,
            time,
            "experiment",
            cycleReceived,
            Solver,
            number,
        )

        # except:
        #    pass

