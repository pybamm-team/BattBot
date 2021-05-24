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

    while True:

        try:

            models = [
                pybamm.lithium_ion.DFN(),
                pybamm.lithium_ion.SPM(),
                pybamm.lithium_ion.SPMe(),
                pybamm.lithium_ion.NewmanTobias(),
                pybamm.lithium_ion.Yang2017(),
            ]

            modelNum = random.randint(0, len(models) - 1)
            model = models[modelNum]
            model = models[0]
            print(model)

            chemistries = [
                pybamm.parameter_sets.Chen2020,
                pybamm.parameter_sets.Marquis2019,
                pybamm.parameter_sets.Ecker2015,
                pybamm.parameter_sets.Ramadass2004
            ]

            chemNum = random.randint(0, len(chemistries) - 1)
            chemistry = chemistries[chemNum]
            chemistry = chemistries[0]
            print(chemistry)

            parameter_values = [
                pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020),
                pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Marquis2019),
                pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Mohtat2020),
                pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Ramadass2004),
                pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Ecker2015)
            ]

            random.shuffle(parameter_values)

            solvers = [
                pybamm.CasadiSolver(mode="safe"),
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

            choice = random.randint(0, 2)
            # choice = 2
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

                    return (
                        model,
                        parameter_values,
                        time,
                        chemistry,
                        solver,
                        False,
                        None, 
                        None,
                        False
                    ) 

            elif choice == 1:
                (
                    cycleReceived,
                    number,
                ) = experiment_generator()
                experiment = pybamm.Experiment(cycleReceived * number)
                (sim, solution, parameter_values) = experiment_solver(model, experiment, chemistry, solver)
                time = plot_graph(solution, sim)
                return (
                    model,
                    parameter_values,
                    time,
                    chemistry,
                    solver,
                    True,
                    cycleReceived,
                    number,
                    False
                )

            elif choice == 2:
                
                number_of_comp = random.randint(2, 3)
                number_of_experiments = random.randint(0, number_of_comp)
                models_for_comp = models[:number_of_comp]
                random.shuffle(models_for_comp)
                parameter_values_for_comp = parameter_values[:number_of_comp]
                models_for_comp = dict(list(enumerate(models_for_comp)))
                parameter_values_for_comp = dict(list(enumerate(parameter_values_for_comp)))
                
                # TODO: Implement Experiments
                # cycles = []
                # numbers = []
                # for i in range(0, number_of_experiments):
                #     (
                #     cycle,
                #     number,
                #     ) = experiment_generator()
                #     print(cycle)
                #     cycles.append(pybamm.Experiment(cycle * number))
                #     numbers.append(number)

                # final_cycles = dict(list(enumerate(cycles)))

                s = pybamm.BatchStudy(
                    models=models_for_comp, 
                    # experiments=final_cycles,
                    parameter_values=parameter_values_for_comp,
                    permutations=True
                )
                s.solve([0, 3700])

                time = plot_graph(sim=s.sims)

                return (   
                    models_for_comp,
                    parameter_values_for_comp,
                    time,
                    None,
                    None,
                    False,
                    None,
                    None,
                    True
                )
        except:
           pass
