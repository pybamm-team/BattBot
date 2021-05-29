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
            ]

            modelNum = random.randint(0, len(models) - 1)
            model = models[modelNum]
            # model = models[0]

            chemistries = [
                pybamm.parameter_sets.Chen2020,
                pybamm.parameter_sets.Marquis2019,
                pybamm.parameter_sets.Ecker2015,
                pybamm.parameter_sets.Ramadass2004
            ]

            chemNum = random.randint(0, len(chemistries) - 1)
            chemistry = chemistries[chemNum]
            # chemistry = chemistries[0]

            solvers = [
                pybamm.CasadiSolver(mode="safe"),
                pybamm.CasadiSolver(mode="fast with events"),
            ]

            solverNum = random.randint(0, len(solvers) - 1)
            # solver = solvers[solverNum]
            solver = solvers[0]

            (
                lower_voltage,
                ambient_temp,
                initial_temp,
                reference_temp,
            ) = chemistry_generator(chemistry)

            choice = random.randint(0, 2)
            
            if choice == 0:
                
                c_rate = random.randint(0, 3)
                (parameter_values, sim, solution) = model_generator(
                    model=model,
                    chemistry=chemistry,
                    solver=solver,
                    c_rate=c_rate,
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
                
                number_of_comp = random.randint(1, 3)
                # number_of_experiments = random.randint(0, number_of_comp)
                random.shuffle(models)
                models_for_comp = models[:number_of_comp]
                models_for_comp = dict(list(enumerate(models_for_comp)))
                params = pybamm.ParameterValues(chemistry=chemistry)
                parameter_values_for_comp = dict(list(enumerate([params])))       

                # TODO: Implement Experiment Comparisons?
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

                # final_cycles = {
                #     0: experiment,
                #     1: experiment2
                # }
                if number_of_comp == 1:
                    param_list = []
                    diff_params = random.randint(2, 3)
                    print(diff_params)
                    for i in range(0, diff_params):
                        param_list.append(params.copy())
                        param_list[i]["Current function [A]"] = random.randint(1, 5)
                    parameter_values_for_comp = dict(list(enumerate(param_list)))

                s = pybamm.BatchStudy(
                    models=models_for_comp,
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
