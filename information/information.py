import pybamm


def information(chemistry, model, solver, isExperiment, cycle, number, isComparison):

    if isExperiment:
        return str(cycle) + " * " + str(number) + " " + str(model) + " " + str(chemistry['citation'])

    elif isComparison:
        return str(model)
    else:    
        return str(model) + " " + str(chemistry['citation']) + " " + str(solver)