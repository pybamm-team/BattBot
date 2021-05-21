import pybamm


def information(chemistry, model, solver, isExperiment, cycle, number):

    if isExperiment:
        return str(cycle) + " * " + str(number) + " " + str(model) + " " + str(chemistry['citation'])

    else:    
        return str(model) + " " + str(chemistry['citation']) + " " + str(solver)