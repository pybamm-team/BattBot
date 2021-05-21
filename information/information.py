import pybamm


def information(chemistry, model):

    if chemistry == pybamm.parameter_sets.Chen2020:
        return "This is some basic information about Chen2020 parameters in a simple " + str(model) + " model plotted using PyBaMM"
    elif chemistry == pybamm.parameter_sets.Marquis2019:
        return "This is some basic information about Marquis2019 parameters in a simple " + str(model) + " model plotted using PyBaMM"
    elif chemistry == pybamm.parameter_sets.Ecker2015:
        return "This is some basic information about Ecker2015 parameters in a simple " + str(model) + " model plotted using PyBaMM"
    elif chemistry == pybamm.parameter_sets.Mohtat2020:
        return "This is some basic information about Mohtat2020 parameters in a simple " + str(model) + " model plotted using PyBaMM"
  