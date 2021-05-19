import pybamm
import random


def model_generator(
    current_function,
    lower_voltage,
    upper_voltage,
    ambient_temp,
    initial_temp,
    reference_temp,
    parameter_number
):

    parameter_number = random.randint(0, 3)

    if parameter_number == 0:
        chemistry = pybamm.parameter_sets.Chen2020
    elif parameter_number == 1:
        chemistry = pybamm.parameter_sets.Marquis2019
    elif parameter_number == 2:
        chemistry = pybamm.parameter_sets.Ecker2015
    elif parameter_number == 3:
        chemistry = pybamm.parameter_sets.Mohtat2020

    models = [
        pybamm.lithium_ion.DFN(), pybamm.lithium_ion.SPM(),
        pybamm.lithium_ion.SPMe(), pybamm.lithium_ion.NewmanTobias(),
        pybamm.lithium_ion.Yang2017(), pybamm.lithium_ion.BasicDFN(),
        pybamm.lithium_ion.BasicSPM()
    ]

    modelNum = random.randint(0, len(models))
    model = models[modelNum]
    print(model)
    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    parameter_values["Current function [A]"] = current_function
    parameter_values["Lower voltage cut-off [V]"] = lower_voltage
    parameter_values["Upper voltage cut-off [V]"] = upper_voltage
    parameter_values["Ambient temperature [K]"] = ambient_temp
    parameter_values["Initial temperature [K]"] = initial_temp
    parameter_values["Reference temperature [K]"] = reference_temp


    sim = pybamm.Simulation(model, parameter_values=parameter_values)
    sim.solve([0, 3600])
    solution = sim.solution

    return parameter_values, sim, solution, model