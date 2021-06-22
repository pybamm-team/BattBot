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
        provided_choice: numerical
            default: None
            Should be used only during testing, using this one can test
            different parts of this function deterministically without relying
            on the random functions to execute that part.
    """
    params = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([params])))
    comparison_dict = {}

    # generate a list of parameter values by varying a single parameter
    # if only 1 model is selected
    param_to_vary = ""
    if number_of_comp == 1:

        param_to_vary = "Current function [A]"

        param_list = []
        diff_params = random.randint(2, 3)
        min_param_value = 100
        for i in range(0, diff_params):
            # copy the original values and append them in the list
            param_list.append(params.copy())

            # generate a random value
            param_value = parameter_value_generator(
                chemistry, param_to_vary
            )

            # change a parameter value
            param_list[i][
                "Current function [A]"
            ] = param_value

            # find the minimum value if "Current function [A]" is varied
            if param_to_vary == "Current function [A]":
                if param_value < min_param_value:
                    min_param_value = param_value

        parameter_values_for_comp = dict(
            list(enumerate(param_list))
        )

    # 0: no experiment
    # 1: experiment
    choice = random.randint(0, 1)

    # if testing, don't select simulations randomly
    if provided_choice is not None:
        choice = provided_choice

    if choice == 0:
        s = pybamm.BatchStudy(
            models=models_for_comp,
            parameter_values=parameter_values_for_comp,
            permutations=True,
        )

        # default t_end
        t_end = 3700

        # if "Current function [A]" is varied, change the t_end
        if param_to_vary == "Current function [A]":
            factor = min_param_value/params[param_to_vary]
            t_end = (1 / factor * 1.1) * 3600

        s.solve([0, t_end])

        # create the GIF
        solution = s.sims[0].solution
        time_array = plot_graph(solution=solution, sim=s.sims)

        comparison_dict.update({
            "model": models_for_comp,
            "parameter_values": params,
            "time_array": time_array,
            "chemistry": chemistry
        })

        return comparison_dict

    elif choice == 1:

        while True:
            try:
                # generate a random cycle and a number for experiment
                cycle = experiment_generator()
                number = random.randint(1, 3)

                # if testing, use the following configuration
                if provided_choice is not None:
                    parameter_values_for_comp = {
                        "Chen2020": pybamm.ParameterValues(
                            chemistry=pybamm.parameter_sets.Chen2020
                        )
                    }
                    cycle = [
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

                # find the max "Time [s]" from all the solutions for the GIF
                max_time = 0
                solution = s.sims[0].solution
                for sim in s.sims:
                    if sim.solution["Time [s]"].entries[-1] > max_time:
                        max_time = sim.solution["Time [s]"].entries[-1]
                        solution = sim.solution

                # create the GIF
                time_array = plot_graph(
                    solution=solution,
                    sim=s.sims
                )

                comparison_dict.update({
                    "model": models_for_comp,
                    "parameter_values": params,
                    "time_array": time_array,
                    "chemistry": chemistry
                })

                return comparison_dict

            except Exception as e:  # pragma: no cover
                print(e)
