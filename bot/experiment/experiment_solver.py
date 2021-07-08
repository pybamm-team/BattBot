import pybamm


def experiment_solver(
    model,
    experiment,
    chemistry,
    solver,
    param_values,
    degradation_parameter
):
    """
    This function simulates and solves experiments with a given model,
    chemistry.
    Parameters:
        model: pybamm.BaseModel
        experiment: pybamm.Experiment
        chemistry: dict
        solver: pybamm.BaseSolver
        param_values: list
            First element should be the parameter values with a varied
            parmeter and the second element should be the varied value.
        degradation_parameter: str
            Parameter that has been varied in param_values.
    Returns:
        sim: pybamm.Simulation
        solutions: list
        labels: list
    """

    solutions = []
    labels = []
    for i in range(0, len(param_values)):

        labels.append(degradation_parameter + ": " + str(param_values[i][1]))

        sim = pybamm.Simulation(
            model=model,
            experiment=experiment,
            parameter_values=param_values[i][0],
            solver=solver,
        )
        if chemistry == pybamm.parameter_sets.Ai2020:
            sim.solve(calc_esoh=False)
        else:
            sim.solve()
        solution = sim.solution
        solutions.append(solution)

    return sim, solutions, labels
