import pybamm
import random
import logging
from utils.parameter_value_generator import parameter_value_generator
from plotting.plot_graph import plot_graph


def comparison_generator(
    number_of_comp,
    models_for_comp,
    chemistry,
    is_experiment,
    cycle=None,
    number=None,
    param_to_vary=None,
):
    """
    Generates a random comparison plot.
    Parameters:
        number_of_comp: numerical
            Number of models be used in the comparison plot.
        models_for_comp: dict
            Different models that are to be used in the comparison plot.
        chemistry: dict
            A single chemistry value which will be used in the comparison
            plot.
        is_experiment: bool
        cycle: list
        number: numerical
        param_to_vary: str
    """
    parameter_values = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([parameter_values])))
    comparison_dict = {}

    # logging configuration
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    labels = []
    varied_values = []
    if number_of_comp == 1:

        param_list = []
        diff_params = random.randint(2, 3)
        min_param_value = 100
        for i in range(0, diff_params):

            # generate parameter values
            if (
                param_to_vary == "Electrode height [m]"
                or param_to_vary == "Electrode width [m]"
            ):
                params, varied_value = parameter_value_generator(
                    parameter_values.copy(),
                    param_to_vary,
                    lower_bound=0.1
                )
            elif param_to_vary == "Ambient temperature [K]":
                params, varied_value = parameter_value_generator(
                    parameter_values.copy(),
                    param_to_vary,
                    lower_bound=265,
                    upper_bound=355
                )
            else:
                params, varied_value = parameter_value_generator(
                    parameter_values.copy(), param_to_vary
                )
            varied_values.append(varied_value)

            logger.info(
                param_to_vary + ": " + str(varied_value)
            )

            labels.append(param_to_vary + ": " + str(varied_value))

            param_list.append(params.copy())

            # find the minimum value if "Current function [A]"
            # is varied
            if param_to_vary == "Current function [A]":
                if varied_value < min_param_value:
                    min_param_value = varied_value

        parameter_values_for_comp = dict(
            list(enumerate(param_list))
        )

    if not is_experiment:

        # vary "Current function [A]" and "Ambient temperature [K]"
        # if comparing models with a constant discharge
        if number_of_comp != 1:
            params, min_param_value = parameter_value_generator(
                parameter_values.copy(), "Current function [A]"
            )
            (
                final_params,
                varied_value_temp
            ) = parameter_value_generator(
                params.copy(),
                "Ambient temperature [K]",
                lower_bound=265,
                upper_bound=355
            )
            parameter_values_for_comp = dict(
                list(enumerate([final_params]))
            )

        batch_study = pybamm.BatchStudy(
            models=models_for_comp,
            parameter_values=parameter_values_for_comp,
            permutations=True,
        )

        # if "Current function [A]" is varied, change the t_end
        if min_param_value != 100:
            factor = min_param_value / parameter_values[
                "Current function [A]"
            ]
            t_end = (1 / factor * 1.1) * 3600
        else:
            # default t_end
            t_end = 3700

        batch_study.solve([0, t_end])

    elif is_experiment:

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

        batch_study = pybamm.BatchStudy(
            models=models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=experiment,
            permutations=True,
        )

        if chemistry == pybamm.parameter_sets.Ai2020:
            batch_study.solve(calc_esoh=False)
        else:
            batch_study.solve()

    # find the max "Time [s]" from all the solutions for the GIF
    max_time = 0
    solution = batch_study.sims[0].solution
    for sim in batch_study.sims:
        if sim.solution["Time [s]"].entries[-1] > max_time:
            max_time = sim.solution["Time [s]"].entries[-1]
            solution = sim.solution

    # create the GIF
    if len(labels) == 0:
        plot_graph(
            solution=solution, sim=batch_study.sims
        )
    else:
        plot_graph(
            solution=solution, sim=batch_study.sims, labels=labels
        )

    comparison_dict.update({
        "varied_values": varied_values,
        "params": parameter_values_for_comp
    })

    return comparison_dict
