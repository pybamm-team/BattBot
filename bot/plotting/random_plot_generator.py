import logging

import pybamm

from plotting.comparison_generator import ComparisonGenerator
from plotting.config_generator import config_generator
from plotting.degradation_comparison_generator import DegradationComparisonGenerator


def random_plot_generator(return_dict, choice, reply_config=None, testing=False):
    """
    Generates a random plot.

    Parameters
    ----------
        return_dict : dict
            A shared dictionary in which all the return values are stored.
        choice : str
            Can be "model comparison", "parameter comparison" or
            "degradation comparison".
        reply_config : dict
            Should be passed when the bot is replying to a requested
            simulation tweet.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    while True:
        try:
            config = config_generator(choice) if reply_config is None else reply_config

            if not testing:
                pybamm.set_logging_level("NOTICE")
                logger.info(config)

            if choice == "degradation comparison":
                degradation_comparison_generator = DegradationComparisonGenerator(
                    config["model"],
                    config["chemistry"],
                    config["param_values"],
                    config["degradation_parameter"],
                    config["cycle"],
                    config["number"],
                )

                # solving the configuration and creating the plot
                degradation_comparison_generator.solve()
                degradation_comparison_generator.generate_summary_variables()

                return_dict.update(
                    {
                        "model": config["model"],
                        "chemistry": config["chemistry"],
                        "is_experiment": True,
                        "cycle": config["cycle"],
                        "number": config["number"],
                        "is_comparison": False,
                        "param_to_vary": config["degradation_parameter"],
                        "varied_values": config["varied_values"],
                        "degradation_mode": config["degradation_mode"],
                        "degradation_value": config["degradation_value"],
                    }
                )

                return

            else:
                # create an object of ComparisonGenerator with the random
                # configuration
                comparison_generator = ComparisonGenerator(
                    config["models_for_comp"],
                    config["chemistry"],
                    config["is_experiment"],
                    config["params"],
                    config["cycle"],
                    config["number"],
                    config["param_to_vary_info"],
                    config["varied_values_override"],
                )

                # create a GIF
                if choice == "model comparison":
                    comparison_generator.model_comparison(testing=testing)
                elif choice == "parameter comparison":
                    comparison_generator.parameter_comparison(testing=testing)

                return_dict.update(
                    {
                        "model": config["models_for_comp"],
                        "chemistry": config["chemistry"],
                        "is_experiment": config["is_experiment"],
                        "cycle": config["cycle"],
                        "number": config["number"],
                        "is_comparison": True,
                        "param_to_vary": next(iter(config["param_to_vary_info"].keys()))
                        if config["param_to_vary_info"] is not None
                        else None,
                        "varied_values": comparison_generator.comparison_dict[
                            "varied_values"
                        ],
                        "params": comparison_generator.comparison_dict["params"],
                    }
                )

                return

        except Exception as e:  # pragma: no cover
            print(e)
