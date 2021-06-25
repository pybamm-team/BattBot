import pybamm


def experiment_solver(model, experiment, chemistry, solver):
    """
    This function simulates and solves an experiment with the
    a given model, chemistry and solver.
    Parameters:
        model: pybamm.BaseModel
        experiment: pybamm.Experiment
        chemistry: dict
        solver: pybamm.BaseSolver
    Returns:
        sim: pybamm.Simulation
        solution: pybamm.Simulation.solution
        parameter_values: pybamm.ParameterValues
    """

    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    sim = pybamm.Simulation(
        model=model,
        experiment=experiment,
        parameter_values=parameter_values,
        solver=solver,
    )
    if chemistry == pybamm.parameter_sets.Ai2020:
        sim.solve(calc_esoh=False)
    else:
        sim.solve()
    solution = sim.solution

    return sim, solution, parameter_values
