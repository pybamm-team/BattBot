import pybamm


def experiment_solver(
    model, experiment, chemistry, param_values, degradation_parameter
):
    """
    This function simulates and solves experiments with a given model,
    chemistry.
    Parameters:
        model: pybamm.BaseModel
        experiment: pybamm.Experiment
        chemistry: dict
        param_values: list
            A list of ParameterValues with each element having a varied
            value for degradation_parameter.
        degradation_parameter: str
            Parameter that has been varied in param_values.
    Returns:
        sim: pybamm.Simulation
        solutions_and_labels: list
    """

    solutions_and_labels = []
    varied_values = []
    for i in range(0, len(param_values)):

        sim = pybamm.Simulation(
            model=model,
            experiment=experiment,
            parameter_values=param_values[i],
        )
        if chemistry == pybamm.parameter_sets.Ai2020:
            sim.solve(calc_esoh=False)
        elif chemistry == pybamm.parameter_sets.Mohtat2020:
            sim.solve(initial_soc=1)
        else:
            sim.solve()
        solution = sim.solution

        # storing solution with the corresponding label
        solutions_and_labels.append(
            [
                solution,
                degradation_parameter
                + ": "
                + str(param_values[i][degradation_parameter]),
            ]
        )
    return sim, solutions_and_labels
