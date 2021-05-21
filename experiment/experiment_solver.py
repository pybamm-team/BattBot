import pybamm

def experiment_solver(model, experiment, chemistry, solver):
    
    sim = pybamm.Simulation(model=model, experiment=experiment,
    chemistry=chemistry, solver=solver)
    sim.solve()
    solution = sim.solution()

    return sim, solution