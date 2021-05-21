import pybamm
import random


def model_generator(
    model,
    chemistry,
    solver,
    current_function,
    lower_voltage,
    upper_voltage,
    ambient_temp,
    initial_temp,
    reference_temp,
):

    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    parameter_values["Current function [A]"] = current_function
    parameter_values["Lower voltage cut-off [V]"] = lower_voltage
    parameter_values["Upper voltage cut-off [V]"] = upper_voltage
    parameter_values["Ambient temperature [K]"] = ambient_temp
    parameter_values["Initial temperature [K]"] = initial_temp
    parameter_values["Reference temperature [K]"] = reference_temp


    sim = pybamm.Simulation(model, parameter_values=parameter_values, solver=solver)
    sim.solve([0, 3600])
    solution = sim.solution

    return parameter_values, sim, solution