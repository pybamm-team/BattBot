import pybamm
import random
from utils.chemistry_generator import chemistry_generator
from plotting.plot_graph import plot_graph
from experiment.experiment_generator import experiment_generator

def comparison_generator(
    number_of_comp,
    models_for_comp,
    chemistry,
    provided_number_of_comp=None,
    testing=False,
):
    params = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([params])))
    comparison_dict = {}

    if (
        number_of_comp == 1
        or (
            testing
            and provided_number_of_comp == 1
        )
    ):
        param_list = []
        diff_params = random.randint(2, 3)
        for i in range(0, diff_params):
            param_list.append(params.copy())
            param_list[i][
                "Current function [A]"
            ] = chemistry_generator(
                chemistry, "Current function [A]"
            )
        parameter_values_for_comp = dict(
            list(enumerate(param_list))
        )

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

    else:

        choice = random.randint(0, 1)

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

        elif choice == 1:

            cycle = experiment_generator()
            number = random.randint(1, 3)
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

            time_array = plot_graph(sim=s.sims)

            comparison_dict["model"] = models_for_comp
            comparison_dict["parameter_values"] = params
            comparison_dict["time_array"] = time_array
            comparison_dict["chemistry"] = chemistry

    return comparison_dict
