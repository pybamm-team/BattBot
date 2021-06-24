import pybamm
from utils.parameter_value_generator import parameter_value_generator


def experiment_solver(
    model,
    experiment,
    chemistry,
    solver,
    number_of_comp
):
    """
    This function simulates and solves an experiment with a given model,
    chemistry and solver.
    Parameters:
        model: pybamm.BaseModel
        experiment: pybamm.Experiment
        chemistry: dict
        solver: pybamm.BaseSolver
        number_of_comp: numerical
            Set it 1 if there are no comparisons to be made, 2 if there are 2
            parameter values you want to compare and so on.
    Returns:
        sim: pybamm.Simulation
        solutions: list
        parameter_values: pybamm.ParameterValues
    """

    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    solutions = []
    param_list = []
    param_to_vary = "Current function [A]"
    for i in range(0, number_of_comp):
        # copy the original values and append them in the list
        param_list.append(parameter_values.copy())

        # generate a random value
        param_value = parameter_value_generator(
            chemistry, param_to_vary
        )

        print(param_to_vary + " " + str(param_value))

        # change a parameter value
        param_list[i][
            param_to_vary
        ] = param_value

        sim = pybamm.Simulation(
            model=model,
            experiment=experiment,
            parameter_values=param_list[i],
            solver=solver,
        )
        if chemistry == pybamm.parameter_sets.Ai2020:
            sim.solve(calc_esoh=False)
        else:
            sim.solve()
        solution = sim.solution
        solutions.append(solution)

    return sim, solutions, parameter_values
