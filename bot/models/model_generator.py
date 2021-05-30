import pybamm


def model_generator(
    model,
    chemistry,
    solver,
    c_rate,
    lower_voltage,
    ambient_temp,
    initial_temp,
    reference_temp,
):
    """
    Simulates and solves a model with given chemistry, solver,
    C_rate, "Lower voltage cut-off [V]", "Ambient temperature [K]",
    "Initial temperature [K]" and "Reference temperature [K]".
    Parameters:
        model: pybamm.BaseModel
        chemistry: dict
        solver: pybamm.BaseSolver
        c_rate: numerical
        lower_voltage: numerical
        ambient_temp: numerical
        initial_temp: numerical
        reference_temp: numerical
    Returns:
        parameter_values: pybamm.ParameterValues
        sim: pybamm.Simulation
        solution: pybamm.Simulation.solution
    """

    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    parameter_values["Lower voltage cut-off [V]"] = lower_voltage
    parameter_values["Ambient temperature [K]"] = ambient_temp
    parameter_values["Initial temperature [K]"] = initial_temp
    parameter_values["Reference temperature [K]"] = reference_temp

    sim = pybamm.Simulation(
        model, parameter_values=parameter_values, solver=solver, C_rate=c_rate
    )
    sim.solve([0, 3700])
    solution = sim.solution

    return parameter_values, sim, solution
