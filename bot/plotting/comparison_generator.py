import pybamm
import random
from utils.parameter_value_generator import parameter_value_generator
from plotting.plot_graph import plot_graph


class ComparisonGenerator:
    def __init__(
        self,
        number_of_comp,
        models_for_comp,
        chemistry,
        is_experiment,
        cycle=None,
        number=None,
        param_to_vary=None,
        bounds=None,
    ):
        self.number_of_comp = number_of_comp
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

    def create_gif(self, batch_study, labels=[]):
        """
        Creates a GIF using the provided pybamm.BatchStudy object
        Parameters:
            batch_study: pybamm.BatchStudy
            labels: list
                To override the default pybamm plot labels
        """
        # find the max "Time [s]" from all the solutions for the GIF
        max_time = 0
        solution = batch_study.sims[0].solution
        for sim in batch_study.sims:
            if sim.solution["Time [s]"].entries[-1] > max_time:
                max_time = sim.solution["Time [s]"].entries[-1]
                solution = sim.solution

        # create the GIF
        if len(labels) == 0:
            plot_graph(solution=solution, sim=batch_study.sims)
        else:
            plot_graph(solution=solution, sim=batch_study.sims, labels=labels)

    def calculate_t_end(self, parameter_values_for_comp):
        """
        Calculates the t_end for t_eval (t_eval=[0, t_end])
        Parameter:
            parameter_values_for_comp: dict
                Of the form -
                {
                    0: pybamm.ParameterValues,
                    1: pybamm.ParameterValues
                }
        """
        # find the minimum value for "Current function [A]"
        min_curr_value = min(
            [
                item["Current function [A]"]
                for k, item in parameter_values_for_comp.items()
            ]
        )
        factor = min_curr_value / self.parameter_values["Current function [A]"]
        t_end = (1 / factor * 1.1) * 3600

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

        # convert the list containing parameter values to a
        # dictionary for pybamm.BatchStudy
        parameter_values_for_comp = dict(
            list(
                enumerate([params if not self.is_experiment else self.parameter_values])
            )
        )

        t_end = self.calculate_t_end(parameter_values_for_comp)

        # convert the list containing parameter values to a
        # dictionary for pybamm.BatchStudy
        parameter_values_for_comp = dict(list(enumerate([params])))

        batch_study = pybamm.BatchStudy(
            models=self.models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=self.experiment,
            permutations=True,
        )

        if self.chemistry == pybamm.parameter_sets.Ai2020 and self.is_experiment:
            batch_study.solve(calc_esoh=False)
        else:
            batch_study.solve([0, t_end])

        self.create_gif(batch_study)

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

        # calculate t_end if varying "Current function [A]"
        if self.param_to_vary == "Current function [A]":
            t_end = self.calculate_t_end(parameter_values_for_comp)
        else:
            t_end = 3700

        batch_study = pybamm.BatchStudy(
            models=self.models_for_comp,
            parameter_values=parameter_values_for_comp,
            experiments=self.experiment,
            permutations=True,
        )

        if self.chemistry == pybamm.parameter_sets.Ai2020 and self.is_experiment:
            batch_study.solve(calc_esoh=False)
        else:
            batch_study.solve([0, t_end])

        self.create_gif(batch_study, labels=labels)

        self.comparison_dict.update(
            {"varied_values": varied_values, "params": parameter_values_for_comp}
        )
