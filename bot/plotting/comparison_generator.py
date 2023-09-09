import os
import random

import pybamm

from utils.parameter_value_generator import parameter_value_generator
from utils.resize_gif import resize_gif


class ComparisonGenerator:
    """
    Generates a GIF comparing 2 or more configurations using the random values provided.

    Parameters
    ----------

        models_for_comp : dict
            Models to be used in comparison. Should be of the form -
            {
                0: pybamm.BaseBatteryModel,
                1: pybamm.BaseBatteryModel
            }
            Provide only 1 model for "parameter comparison" and 2 or more models for
            "model comparison".
        chemistry : str
            A PyBaMM chemistry.
        is_experiment : bool
            If the comparison includes an experiment.
        params : pybamm.ParameterValues
            ParameterValues to be used in the comparisons.
        cycle : list
            default : None
            Single cycle of the experiment. Provide only when the comparison includes an
            experiment.
        number : numerical
            default : None
            The number with which the cycle is being multiplied. Provide only when the
            comparison includes an experiment.
        param_to_vary_info : dict
            default : None
            Information about parameter which is to be varied in "parameter comparison".
            Provide only when the comparison is of type "parameter comparison". Should
            be of the form -
            {
                parameter: {
                    "print_name": str,
                    "bounds": (numerical, numerical)
                }
            }
        varied_values_override : list
            default : None
            A list of varied values which will override the default random values. To be
            used while replying.
    """

    def __init__(
        self,
        models_for_comp,
        chemistry,
        is_experiment,
        params,
        cycle=None,
        number=None,
        param_to_vary_info=None,
        varied_values_override=None,
    ):
        self.models_for_comp = models_for_comp
        self.chemistry = chemistry
        self.is_experiment = is_experiment
        self.cycle = cycle
        self.number = number
        self.param_to_vary = (
            next(iter(param_to_vary_info.keys()))
            if param_to_vary_info is not None
            else None
        )
        self.bounds = (
            next(iter(param_to_vary_info.values()))["bounds"]
            if param_to_vary_info is not None
            else None
        )
        self.print_name = (
            next(iter(param_to_vary_info.values()))["print_name"]
            if param_to_vary_info is not None
            else None
        )
        self.parameter_values = pybamm.ParameterValues(self.chemistry)
        self.experiment = (
            dict(list(enumerate([pybamm.Experiment(self.cycle * self.number)])))
            if self.cycle is not None
            else None
        )
        self.comparison_dict = {}
        self.params = params
        self.varied_values_override = varied_values_override

    def calculate_t_end(self, parameter_values_for_comp, force=False):
        """
        Calculates the t_end for t_eval (t_eval=[0, t_end]).

        Parameters
        ----------
            parameter_values_for_comp : dict
                Of the form -
                {
                    0: pybamm.ParameterValues,
                    1: pybamm.ParameterValues
                }
            force : bool
                default : False
                To be used to force the calculation of t_end.
        """
        # find the minimum value for "Current function [A]"
        if self.param_to_vary == "Current function [A]" or force:
            # find the minimum value for "Current function [A]"
            min_curr_value = min(
                [
                    item["Current function [A]"]
                    for k, item in parameter_values_for_comp.items()
                ]
            )
            factor = min_curr_value / self.parameter_values["Current function [A]"]
            t_end = (1 / factor * 1.1) * 3600
        else:
            t_end = 3700

        return t_end

    def create_gif(self, batch_study, testing=False):
        """
        Create and resize a GIF.

        Parameters
        ----------
        batch_study : :class:`pybamm.BatchStudy`
            Object of BatchStudy.
        testing : bool
            default : False
            To be used while testing to generate less number of plots.
        """
        if not testing:
            batch_study.create_gif()
        else:
            batch_study.create_gif(number_of_images=3, duration=1)

        # resizing the GIF for Twitter
        resize_gif("plot.gif", resize_to=(1440, 1440))

        if os.path.getsize("plot.gif") >= 15728640:  # pragma: no cover
            resize_gif("plot.gif", resize_to=(1080, 1080))

    def model_comparison(self, testing=False):
        """
        Generates a comparison GIF with 2 or more models.
        """
        # convert the list containing parameter values to a
        # dictionary for pybamm.BatchStudy
        parameter_values_for_comp = dict(list(enumerate([self.params])))

        batch_study = pybamm.BatchStudy(
            models=self.models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=self.experiment,
            permutations=True,
        )

        if self.is_experiment:
            if self.chemistry == "Ai2020":
                batch_study.solve(calc_esoh=False)
            else:
                batch_study.solve()
        else:
            t_end = self.calculate_t_end(parameter_values_for_comp, force=True)
            batch_study.solve([0, t_end])

        self.create_gif(batch_study, testing)

        self.comparison_dict.update(
            {
                "varied_values": {
                    "Current function [A]": self.params["Current function [A]"],
                    "Ambient temperature [K]": self.params["Ambient temperature [K]"],
                },
                "params": parameter_values_for_comp,
            }
        )

    def parameter_comparison(self, testing=False):
        """
        Generates a comparison with a single model, by varying a single parameter.
        """
        # generate a list of parameter values by varying a single parameter
        labels = []
        varied_values = []
        param_list = []
        # randomly select number of comparisons and vary a
        # parameter value or use the varied_values_override
        # list to change a parameter's value
        diff_params = (
            random.randint(2, 3)
            if self.varied_values_override is None
            else len(self.varied_values_override)
        )
        for i in range(diff_params):
            # generate parameter values
            if self.varied_values_override is None:
                params = parameter_value_generator(
                    self.params.copy(),
                    {self.param_to_vary: self.bounds},
                )
            else:
                params = self.params.copy()
                params[self.param_to_vary] = self.varied_values_override[i]

            # append the varied values in `labels` which will be used
            # in the GIF
            if self.print_name is not None:
                val = float(params[self.param_to_vary].__str__())
                labels.append(
                    self.print_name
                    + " * "
                    + (f"{val:.5e}" if val > 10 or val < 1 and val != 0 else str(val))
                )
                varied_values.append(float(params[self.param_to_vary].__str__()))
            else:
                val = params[self.param_to_vary]
                labels.append(
                    self.param_to_vary
                    + ": "
                    + (f"{val:.5e}" if val > 10 or val < 1 and val != 0 else str(val))
                )
                varied_values.append(params[self.param_to_vary])

            # create a list of ParameterValues with each element
            # having the same parameter varied
            param_list.append(params)

        # convert the list containing parameter values to a dictionary
        # for pybamm.BatchStudy
        parameter_values_for_comp = dict(list(enumerate(param_list)))

        batch_study = pybamm.BatchStudy(
            models=self.models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=self.experiment,
            permutations=True,
        )

        if self.is_experiment:
            if self.chemistry == "Ai2020":
                batch_study.solve(calc_esoh=False)
            else:
                batch_study.solve()
        else:
            t_end = self.calculate_t_end(parameter_values_for_comp)
            batch_study.solve([0, t_end])

        # call the plot method first to pass labels
        batch_study.plot(labels=labels, testing=True)

        self.create_gif(batch_study, testing)

        self.comparison_dict.update(
            {"varied_values": varied_values, "params": parameter_values_for_comp}
        )
