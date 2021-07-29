import pybamm
import logging
from experiment.experiment_solver import experiment_solver
from plotting.summary_variables import generate_summary_variables
from plotting.comparison_generator import ComparisonGenerator
from plotting.config_generator import config_generator


def random_plot_generator(
    return_dict,
    choice,
    reply_config=None
):
    """
    Generates a random plot.
    Parameters:
        return_dict: dict
            A shared dictionary in which all the return values are stored.
        choice: str
            Can be "model comparison", "parameter comparison" or
            "degradation comparison (summary variables)".
        reply_config: dict
            Should be passed when the bot is replying to a requested
            simulation tweet.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    while True:

        try:
            pybamm.set_logging_level("NOTICE")

            if reply_config is not None:    # pragma: no cover
                config = reply_config
            else:
                config = config_generator(choice)

            logger.info(config)

            if choice == (
                "degradation comparison (summary variables)"
            ):

                if config["chemistry"] == pybamm.parameter_sets.Ai2020:
                    experiment = pybamm.Experiment(
                        config["cycle"] * config["number"]
                    )
                else:
                    experiment = pybamm.Experiment(
                        config["cycle"] * config["number"],
                        termination="80% capacity"
                    )

                # solving
                (
                    sim,
                    solution,
                    parameter_values
                ) = experiment_solver(
                    model=config["model"],
                    experiment=experiment,
                    chemistry=config["chemistry"],
                )

                # plotting summary variables
                generate_summary_variables(solution, config["chemistry"])

                return_dict.update({
                    "model": config["model"],
                    "chemistry": config["chemistry"],
                    "is_experiment": True,
                    "cycle": config["cycle"],
                    "number": config["number"],
                    "is_comparison": False
                })

                return

            else:

                # create an object of ComparisonGenerator with the random
                # configuration
                comparison_generator = ComparisonGenerator(
                    config["models_for_comp"],
                    config["chemistry"],
                    config["is_experiment"],
                    config["cycle"],
                    config["number"],
                    config["param_to_vary"],
                    config["bounds"]
                )

                # create a GIF
                if choice == "model comparison":
                    comparison_generator.model_comparison()
                elif choice == "parameter comparison":
                    comparison_generator.parameter_comparison()

                return_dict.update({
                    "model": config["models_for_comp"],
                    "chemistry": config["chemistry"],
                    "is_experiment": config["is_experiment"],
                    "cycle": config["cycle"],
                    "number": config["number"],
                    "is_comparison": True,
                    "param_to_vary": config["param_to_vary"],
                    "varied_values": comparison_generator.comparison_dict["varied_values"],    # noqa
                    "params": comparison_generator.comparison_dict["params"]    # noqa
                })

                return

        except Exception as e:  # pragma: no cover
            print(e)
