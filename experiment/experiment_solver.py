import pybamm

def experiment_solver(model, experiment, chemistry, solver):
    
    parameter_values = pybamm.ParameterValues(chemistry=chemistry)

    sim = pybamm.Simulation(model=model, experiment=experiment,
    parameter_values=parameter_values, solver=solver)
    sim.solve()
    solution = sim.solution

    return sim, solution, parameter_values