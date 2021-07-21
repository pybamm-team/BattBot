import pybamm
import random
import logging
from utils.parameter_value_generator import parameter_value_generator
from plotting.plot_graph import plot_graph
from experiment.experiment_generator import experiment_generator


param_to_vary_dict = {
    "Current function [A]": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Electrode height [m]": {
        "lower_bound": 0.1,
        "upper_bound": None
    },
    "Electrode width [m]": {
        "lower_bound": 0.1,
        "upper_bound": None
    },
    "Negative electrode conductivity [S.m-1]": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Negative electrode porosity": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Negative electrode active material volume fraction": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Negative electrode Bruggeman coefficient (electrolyte)": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Negative electrode exchange-current density [A.m-2]": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Positive electrode porosity": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Positive electrode exchange-current density [A.m-2]": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Positive electrode Bruggeman coefficient (electrolyte)": {
        "lower_bound": None,
        "upper_bound": None
    },
    "Ambient temperature [K]": {
        "lower_bound": 265,
        "upper_bound": 355
    }
}


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
    parameter_values = pybamm.ParameterValues(chemistry=chemistry)
    parameter_values_for_comp = dict(list(enumerate([parameter_values])))
    comparison_dict = {}

    # logging configuration
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    while True:
        try:

            # if testing, don't select simulations randomly
            if provided_choice is not None:
                choice = provided_choice
            else:
                choice_list = ["experiment", "no experiment"]
                choice = random.choice(choice_list)

            # remove "Current function [A]" from the dict if simulating an
            # experiment and add it back if not an experiment
            # (adding it back because pop edits the original list)
            if (
                choice == "experiment"
                and "Current function [A]" in param_to_vary_dict
            ):
                param_to_vary_dict.pop("Current function [A]")
            elif (
                choice == "no experiment"
                and "Current function [A]" not in param_to_vary_dict
            ):
                param_to_vary_dict.update({
                    "Current function [A]": {
                        "lower_bound": None,
                        "upper_bound": None
                    }
                })

            # generate a list of parameter values by varying a single
            # parameter if only 1 model is selected
            param_to_vary = None
            labels = []
            varied_values = []
            if number_of_comp == 1:

                if provided_param_to_vary is not None:
                    param_to_vary = provided_param_to_vary
                else:
                    param_to_vary = random.choice(
                        list(
                            param_to_vary_dict.keys()
                        )
                    )

                param_list = []
                # randomly select number of comparisons by varying a
                # parameter value
                diff_params = random.randint(2, 3)
                for i in range(0, diff_params):

                    # generate parameter values
                    params = parameter_value_generator(
                        parameter_values.copy(),
                        {
                            param_to_vary: param_to_vary_dict[param_to_vary]
                        }
                    )

                    logger.info(
                        param_to_vary + ": " + str(params[param_to_vary])
                    )

                    # append the varied values in `labels` which will be used
                    # in the GIF
                    labels.append(
                        param_to_vary + ": " + str(params[param_to_vary])
                    )
                    varied_values.append(params[param_to_vary])

                    # create a list of ParameterValues with each element
                    # having the same parameter varied
                    param_list.append(params)

                # convert the list containing parameter values to a dictionary
                # for pybamm.BatchStudy
                parameter_values_for_comp = dict(
                    list(enumerate(param_list))
                )

            if choice == "no experiment":

                is_experiment = False

                # vary "Current function [A]" and "Ambient temperature [K]"
                # if comparing models with a constant discharge
                if number_of_comp != 1:
                    params = parameter_value_generator(
                        parameter_values.copy(),
                        {
                            "Current function [A]":
                            param_to_vary_dict["Current function [A]"],
                            "Ambient temperature [K]":
                            param_to_vary_dict["Ambient temperature [K]"]
                        }
                    )
                    # convert the list containing parameter values to a
                    # dictionary for pybamm.BatchStudy
                    parameter_values_for_comp = dict(
                        list(enumerate([params]))
                    )

                batch_study = pybamm.BatchStudy(
                    models=models_for_comp,
                    parameter_values=parameter_values_for_comp,
                    permutations=True,
                )

                # if "Current function [A]" is varied, change the t_end
                if (
                    param_to_vary == "Current function [A]"
                    or number_of_comp != 1
                ):
                    # find the minimum value for "Current function [A]"
                    min_param_value = min(
                        [
                            item["Current function [A]"]
                            for k, item in parameter_values_for_comp.items()
                        ]
                    )
                    factor = min_param_value / parameter_values[
                        "Current function [A]"
                    ]
                    t_end = (1 / factor * 1.1) * 3600
                else:
                    # default t_end
                    t_end = 3700

                batch_study.solve([0, t_end])

            elif choice == "experiment":

                is_experiment = True

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

                # create a dictionary containing pybamm.Experiment for
                # pybamm.BatchStudy
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
                "model": models_for_comp,
                "chemistry": chemistry,
                "is_experiment": is_experiment,
                "cycle": cycle if is_experiment else None,
                "number": number if is_experiment else None,
                "is_comparison": True,
                "param_to_vary": param_to_vary,
                "varied_values": varied_values,
                "params": parameter_values_for_comp
            })

            return comparison_dict

        except Exception as e:  # pragma: no cover
            print(e)
