import pybamm


def model_solver(
    model,
    chemistry,
    solver,
    c_rate,
    lower_voltage
):
    """
    Simulates and solves a model with given chemistry, solver
    and C_rate.
    Parameters:
        model: pybamm.BaseModel
        chemistry: dict
        solver: pybamm.BaseSolver
        c_rate: numerical
        lower_voltage: numerical
    Returns:
        parameter_values: pybamm.ParameterValues
        sim: pybamm.Simulation
        solution: pybamm.Simulation.solution
    """

    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    parameter_values["Lower voltage cut-off [V]"] = lower_voltage

    sim = pybamm.Simulation(
        model, parameter_values=parameter_values, solver=solver, C_rate=c_rate
    )
    sim.solve([0, 3700])
    solution = sim.solution

    return parameter_values, sim, solution
