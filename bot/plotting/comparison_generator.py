import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator
from plotting.plot_graph import plot_graph
from experiment.experiment_generator import experiment_generator


def comparison_generator(
    number_of_comp,
    models_for_comp,
    chemistry,
    provided_choice=None,
):
    params = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([params])))
    comparison_dict = {}

    if number_of_comp == 1:
        param_list = []
        diff_params = random.randint(2, 3)
        for i in range(0, diff_params):
            param_list.append(params.copy())
            param_list[i][
                "Current function [A]"
            ] = parameter_value_generator(
                chemistry, "Current function [A]"
            )
        parameter_values_for_comp = dict(
            list(enumerate(param_list))
        )

    choice = random.randint(0, 1)
    if provided_choice is not None:
        choice = provided_choice

    if choice == 0:
        s = pybamm.BatchStudy(
            models=models_for_comp,
            parameter_values=parameter_values_for_comp,
            permutations=True,
        )

        s.solve([0, 3700])

        time_array = plot_graph(sim=s.sims)

        comparison_dict["model"] = models_for_comp
        comparison_dict["parameter_values"] = params
        comparison_dict["time_array"] = time_array
        comparison_dict["chemistry"] = chemistry

        return comparison_dict

    elif choice == 1:

        while True:
            try:
                cycle = experiment_generator()
                number = random.randint(1, 3)

                if provided_choice is not None:
                    parameter_values_for_comp = {
                        "Chen2020": pybamm.ParameterValues(
                            chemistry=pybamm.parameter_sets.Chen2020
                        )
                    }
                    experiment = [
                        (
                            "Discharge at C/10 for 10 hours "
                            + "or until 3.3 V",
                            "Rest for 1 hour",
                            "Charge at 1 A until 4.1 V",
                            "Hold at 4.1 V until 50 mA",
                            "Rest for 1 hour"
                        )
                    ]
                    number = 1

                experiment = dict(
                    list(
                        enumerate(
                            [
                                pybamm.Experiment(
                                    cycle * number
                                )
                            ]
                        )
                    )
                )

                s = pybamm.BatchStudy(
                    models=models_for_comp,
                    parameter_values=parameter_values_for_comp,
                    experiments=experiment,
                    permutations=True,
                )

                s.solve()

                max_time = 0
                solution = s.sims[0].solution
                for sim in s.sims:
                    if sim.solution["Time [s]"].entries[-1] > max_time:
                        max_time = sim.solution["Time [s]"].entries[-1]
                        solution = sim.solution

                time_array = plot_graph(
                    solution=solution,
                    sim=s.sims
                )

                comparison_dict["model"] = models_for_comp
                comparison_dict["parameter_values"] = params
                comparison_dict["time_array"] = time_array
                comparison_dict["chemistry"] = chemistry

                return comparison_dict

            except Exception as e:  # pragma: no cover
                print(e)
