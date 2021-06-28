import pybamm
import random
import logging
from utils.parameter_value_generator import parameter_value_generator
from plotting.plot_graph import plot_graph
from experiment.experiment_generator import experiment_generator


def comparison_generator(
    number_of_comp,
    models_for_comp,
    chemistry,
    provided_choice=None,
    provided_param_to_vary=None
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
        provided_choice: str
            default: None
            Should be used only during testing, using this one can test
            different parts of this function deterministically without relying
            on the random functions to execute that part.
        provided_param_to_vary: str
            default: None
            Should be used only during testing, using this one can test
            different parts of this function deterministically without relying
            on the random functions to execute that part.

    """
    params = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([params])))
    comparison_dict = {}

    # logging configuration
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # generate a list of parameter values by varying a single parameter
    # if only 1 model is selected
    param_to_vary = ""
    labels = []
    if number_of_comp == 1:

        param_to_vary_list = [
            "Current function [A]"
            "Electrode height [m]",
            "Electrode width [m]",
            "Negative electrode conductivity [S.m-1]",
            "Negative electrode porosity",
            "Negative electrode active material volume fraction",
            "Negative electrode Bruggeman coefficient (electrolyte)",
            "Negative electrode exchange-current density [A.m-2]",
            "Positive electrode porosity",
            "Positive electrode active material volume fraction",
            "Positive electrode exchange-current density [A.m-2]",
            "Positive electrode Bruggeman coefficient (electrolyte)",
            "Ambient temperature [K]"
        ]

        if provided_param_to_vary is not None:
            param_to_vary = provided_param_to_vary
        else:
            param_to_vary = random.choice(param_to_vary_list)

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
                param_to_vary
            ] = param_value

            logger.info(
                param_to_vary + ": " + str(param_value)
            )

            labels.append(param_to_vary + ": " + str(param_value))

            # find the minimum value if "Current function [A]" is varied
            if param_to_vary == "Current function [A]":
                if param_value < min_param_value:
                    min_param_value = param_value

        parameter_values_for_comp = dict(
            list(enumerate(param_list))
        )

    # if testing, don't select simulations randomly
    if provided_choice is not None:
        choice = provided_choice
    else:
        choice_list = ["experiment", "no experiment"]
        choice = random.choice(choice_list)

    if choice == "no experiment":
        s = pybamm.BatchStudy(
            models=models_for_comp,
            parameter_values=parameter_values_for_comp,
            permutations=True,
        )

        # if "Current function [A]" is varied, change the t_end
        if param_to_vary == "Current function [A]":
            factor = min_param_value / params[param_to_vary]
            t_end = (1 / factor * 1.1) * 3600
        else:
            # default t_end
            t_end = 3700

        s.solve([0, t_end])

        # create the GIF
        solution = s.sims[0].solution
        if len(labels) == 0:
            time_array = plot_graph(
                solution=solution, sim=s.sims
            )
        else:
            time_array = plot_graph(
                solution=solution, sim=s.sims, labels=labels
            )

        comparison_dict.update({
            "model": models_for_comp,
            "parameter_values": params,
            "time_array": time_array,
            "chemistry": chemistry
        })

        return comparison_dict

    elif choice == "experiment":

        while True:
            try:
                # generate a random cycle and a number for experiment
                cycle = experiment_generator()
                number = random.randint(1, 3)

                # if testing, use the following configuration
                if provided_choice is not None:
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

                if chemistry == pybamm.parameter_sets.Ai2020:
                    s.solve(calc_esoh=False)
                else:
                    s.solve()

                # find the max "Time [s]" from all the solutions for the GIF
                max_time = 0
                solution = s.sims[0].solution
                for sim in s.sims:
                    if sim.solution["Time [s]"].entries[-1] > max_time:
                        max_time = sim.solution["Time [s]"].entries[-1]
                        solution = sim.solution

                # create the GIF
                if len(labels) == 0:
                    time_array = plot_graph(
                        solution=solution, sim=s.sims
                    )
                else:
                    time_array = plot_graph(
                        solution=solution, sim=s.sims, labels=labels
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
