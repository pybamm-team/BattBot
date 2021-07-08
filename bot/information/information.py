import pybamm


def information(
    chemistry,
    model,
    is_experiment,
    cycle,
    number,
    is_summary_variable,
    param_to_vary,
    degradation_mode=None,
    degradation_value=None
):
    """
    Generates tweet text.
    Parameters:
        chemistry: dict
        model: pybamm.BaseModel or dict
        is_experiment: bool
        cycle: list or None
        number: numerical or None
        is_comparison: bool
        param_to_vary: str or None
        degradation_mode: str or None
        degradation_values: str or None
    Returns
        tweet_text: str
    """

    params = pybamm.ParameterValues(chemistry=chemistry)
    c_rate = (
        params["Current function [A]"] / params["Nominal cell capacity [A.h]"]
    )
    temp = params["Ambient temperature [K]"] - 273.15

    if is_experiment and is_summary_variable:
        tweet_text = (
            f"Plotting {model.name} with "
            f"{chemistry['citation']} parameters and "
            f"{degradation_value} {degradation_mode}, "
            f"for experiment: {cycle}"
        )

    elif is_experiment:
        if param_to_vary is None:
            if len(model) == 2:
                tweet_text = (
                    f"Comparing {model[0].name} and {model[1].name} "
                    f"with {chemistry['citation']} parameters for the "
                    f"following experiment: {cycle} * {number}"
                )
            else:
                tweet_text = (
                    f"Comparing {model[0].name}, {model[1].name}, and "
                    f"{model[2].name} with {chemistry['citation']} "
                    "parameters for the following experiment: "
                    f"{cycle} * {number}"
                )
        elif param_to_vary is not None:
            tweet_text = (
                f"{model[0].name} with {chemistry['citation']} parameters "
                f"varying {param_to_vary} for the following experiment: "
                f"{cycle} * {number}"
            )
    elif not is_experiment:
        if param_to_vary is None:
            if len(model) == 2:
                tweet_text = (
                    f"Comparing {model[0].name} and {model[1].name} with "
                    f"{chemistry['citation']} parameters for a {c_rate} C "
                    f"discharge at {temp}°C"
                )
            else:
                tweet_text = (
                    f"Comparing {model[0].name}, {model[1].name}, and "
                    f"{model[2].name} with {chemistry['citation']} "
                    f"parameters for a {c_rate} C discharge at {temp}°C"
                )
        elif param_to_vary is not None:
            tweet_text = (
                f"{model[0].name} with {chemistry['citation']} parameters "
                f"varying {param_to_vary} for a {c_rate} C discharge at "
                f"{temp}°C"
            )

    return tweet_text
