import pybamm


def information(chemistry, model, solver, isExperiment, cycle, number):

    if isExperiment:
        return str(cycle) + " * " + str(number) + str(model) + str(chemistry) + str(solver)

    else:    
        return str(model) + str(chemistry) + str(solver)