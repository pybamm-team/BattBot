import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator
from plotting.create_gif import create_gif


class ComparisonGenerator:
    """
    Generates a GIF comparing 2 or more configurations using the random values provided.
    Parameters:
        models_for_comp: dict
            Models to be used in comparison. Should be of the form -
                {
                    0: pybamm.BaseBatteryModel,
                    1: pybamm.BaseBatteryModel
                }
                Provide only 1 model for "parameter comparison" and 2 or more models for
                "model comparison".
        chemistry: dict
            Chemistry for the models.
        is_experiment: bool
            If the comparison includes an experiment.
        cycle: list
            default: None
            Single cycle of the experiment. Provide only when the comparison includes an
            experiment.
        number: numerical
            default: None
            The number with which the cycle is being multiplied. Provide only when the
            comparison includes an experiment.
        param_to_vary: str
            default: None
            The parameter which is to be varied in "parameter comparison". Provide only
            when the comparison is of type "parameter comparison".
        bounds: tuple
            default: None
            The bounds of the parameter which is to be varied in "parameter comparison".
            Provide only when the comparison is of type "parameter comparison".
    """

    def __init__(
        self,
        models_for_comp,
        chemistry,
        is_experiment,
        cycle=None,
        number=None,
        param_to_vary=None,
        bounds=None,
    ):
        self.models_for_comp = models_for_comp
        self.chemistry = chemistry
        self.is_experiment = is_experiment
        self.cycle = cycle
        self.number = number
        self.param_to_vary = param_to_vary
        self.bounds = bounds
        self.parameter_values = pybamm.ParameterValues(chemistry=self.chemistry)
        self.experiment = (
            dict(list(enumerate([pybamm.Experiment(self.cycle * self.number)])))
            if self.cycle is not None
            else None
        )
        self.comparison_dict = {}

    def calculate_t_end(self, parameter_values_for_comp, force=False):
        """
        Calculates the t_end for t_eval (t_eval=[0, t_end]).
        Parameter:
            parameter_values_for_comp: dict
                Of the form -
                {
                    0: pybamm.ParameterValues,
                    1: pybamm.ParameterValues
                }
            force: bool
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

    def model_comparison(self):
        """
        Generates a comparison GIF with 2 or more models
        """
        params = {}
        if not self.is_experiment:
            # vary "Current function [A]" and "Ambient temperature [K]"
            params = parameter_value_generator(
                self.parameter_values.copy(),
                {
                    "Current function [A]": (None, None),
                    "Ambient temperature [K]": (265, 355),
                },
            )

        elif self.is_experiment:
            # vary "Ambient temperature [K]"
            params = parameter_value_generator(
                self.parameter_values.copy(),
                {
                    "Ambient temperature [K]": (265, 355),
                },
            )

        # convert the list containing parameter values to a
        # dictionary for pybamm.BatchStudy
        parameter_values_for_comp = dict(
            list(
                enumerate([params])
            )
        )

        batch_study = pybamm.BatchStudy(
            models=self.models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=self.experiment,
            permutations=True,
        )

        if self.is_experiment:
            batch_study.solve()
        else:
            t_end = self.calculate_t_end(parameter_values_for_comp, force=True)
            batch_study.solve([0, t_end])

        create_gif(batch_study)

        self.comparison_dict.update(
            {"varied_values": [], "params": parameter_values_for_comp}
        )

    def parameter_comparison(self):
        """
        Generates a comparison with a single model, by varying a single parameter
        """
        # generate a list of parameter values by varying a single parameter
        labels = []
        varied_values = []
        param_list = []
        # randomly select number of comparisons and vary a
        # parameter value
        diff_params = random.randint(2, 3)
        for i in range(0, diff_params):

            # generate parameter values
            params = parameter_value_generator(
                self.parameter_values.copy(), {self.param_to_vary: self.bounds}
            )

            # append the varied values in `labels` which will be used
            # in the GIF
            labels.append(self.param_to_vary + ": " + str(params[self.param_to_vary]))
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
            if self.chemistry == pybamm.parameter_sets.Ai2020:
                batch_study.solve(calc_esoh=False)
            else:
                batch_study.solve()
        else:
            t_end = self.calculate_t_end(parameter_values_for_comp)
            batch_study.solve([0, t_end])

        create_gif(batch_study, labels=labels)

        self.comparison_dict.update(
            {"varied_values": varied_values, "params": parameter_values_for_comp}
        )
