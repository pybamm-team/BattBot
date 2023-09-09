import matplotlib.pyplot as plt
import numpy as np
import pybamm


class DegradationComparisonGenerator:
    """
    Generates a summary variable plot comparing 2 or more configurations using the
    random values provided.

    Parameters
    ----------
        model : :class:`pybamm.BaseBatteryModel`
            Model to be used in the comparison.
        chemistry : str
            A PyBaMM chemistry.
        param_values : list
            Parameter values with one degradation parameter varied. Should be of the
            form -
            [
                :class:`pybamm.ParameterValues`,
                :class:`pybamm.ParameterValues`
            ]
        degradation_parameter : str
            The parameter that has been varied in param_values.
        cycle : list
            Experiment cycle to be used in the comparison.
        number : numerical
            Number with which the cycle is multiplied.
    """

    def __init__(
        self,
        model,
        chemistry,
        param_values,
        degradation_parameter,
        cycle,
        number,
    ):
        self.model = model
        self.chemistry = chemistry
        self.param_values = param_values
        self.degradation_parameter = degradation_parameter
        self.cycle = cycle
        self.number = number

    def create_simulation(self, experiment):
        """
        Creates a simulation for the given configuration.

        Parameters
        ----------
            experiment : :class:`pybamm.Experiment`
                The experiment to be simulated.

        Returns
        -------
            sim : :class:`pybamm.Simulation`
            solutions_and_labels : list
                Of the form -
                [
                    [:class:`pybamm.Solution`, label],
                    [:class:`pybamm.Solution`, label]
                ]
        """
        solutions_and_labels = []

        # iterate through all the parameter values, plugging one of them in the
        # simulation every time
        for i in range(len(self.param_values)):
            sim = pybamm.Simulation(
                model=self.model,
                experiment=experiment,
                parameter_values=self.param_values[i],
            )
            if self.chemistry == "Ai2020":  # pragma: no cover
                sim.solve(calc_esoh=False)
            elif self.chemistry == "Mohtat2020":
                sim.solve(initial_soc=1)
            else:  # pragma: no cover
                sim.solve()
            solution = sim.solution

            # storing solution with the corresponding label
            val = self.param_values[i][self.degradation_parameter]
            solutions_and_labels.append(
                [
                    solution,
                    self.degradation_parameter
                    + ": "
                    + (f"{val:.5e}" if val > 10 or val < 1 else str(val)),
                ]
            )
        return sim, solutions_and_labels

    def solve(self):
        """
        Solves an experiment with the given configuration.
        """
        if self.chemistry == "Ai2020":  # pragma: no cover
            experiment = pybamm.Experiment(self.cycle * self.number)
        else:
            experiment = pybamm.Experiment(
                self.cycle * self.number, termination="80% capacity"
            )

        # create a simulation
        sim, solutions_and_labels = self.create_simulation(experiment)

        # sort the solutions and labels in ascending order of the varied value
        solutions_and_labels_sorted = sorted(
            solutions_and_labels, key=lambda x: float(x[1].split(":")[1])
        )

        self.solutions = [x[0] for x in solutions_and_labels_sorted]
        self.labels = [x[1] for x in solutions_and_labels_sorted]

    def generate_summary_variables(self):
        """
        Creates and saves a picture of summary variable comparison plot.
        """
        if self.chemistry == "Ai2020":  # pragma: no cover
            vars_to_plot = [
                "Measured capacity [A.h]",
                "Loss of lithium inventory [%]",
                "Loss of active material in negative electrode [%]",
                "Loss of active material in positive electrode [%]",
            ]
        else:
            vars_to_plot = [
                "Capacity [A.h]",
                "Loss of lithium inventory [%]",
                "Loss of active material in negative electrode [%]",
                "Loss of active material in positive electrode [%]",
                "x_100",
                "x_0",
                "y_100",
                "y_0",
            ]

        # config for subplots
        length = len(vars_to_plot)
        n = int(length // np.sqrt(length))
        m = int(np.ceil(length / n))

        # create subplots
        fig, axes = plt.subplots(n, m, figsize=(15, 8))
        # find max cycle number
        x_max = max(
            [
                solution.summary_variables["Cycle number"][-1]
                for solution in self.solutions
            ]
        )

        # plot the summary variables
        for var, ax in zip(vars_to_plot, axes.flat):
            # iterate through the solutions
            for solution in self.solutions:
                ax.plot(
                    solution.summary_variables["Cycle number"],
                    solution.summary_variables[var],
                )
            ax.set_xlabel("Cycle number")
            ax.set_ylabel(var)
            ax.set_xlim([1, x_max])

        # save the generated plot
        fig.tight_layout()
        fig.legend(self.labels, loc="lower left", bbox_to_anchor=(0.77, -0.08))
        plt.savefig("plot.png", dpi=300, bbox_inches="tight")
