def tweet_text_generator(
    chemistry,
    model,
    is_experiment,
    cycle,
    number,
    is_comparison,
    param_to_vary,
    params
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
        param_to_vary: str or list or None
        params: dict
            To be used when varied values have to be added to the tweet text.
    Returns
        tweet_text: str
        experiment: str or None
    """

    if is_experiment and not is_comparison:
        tweet_text = (
            f"Summary variables for {model.name} with "
            f"{chemistry['citation']} parameters for the following "
            f"experiment: {cycle} * {number}"
        )

    elif is_experiment:
        if param_to_vary is None and is_comparison:
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
        elif param_to_vary is not None and is_comparison:
            tweet_text = (
                f"{model[0].name} with {chemistry['citation']} parameters "
                f"varying '{param_to_vary}' for the following experiment: "
                f"{cycle} * {number}"
            )
    elif not is_experiment:

        c_rate = round(
            params[0]["Current function [A]"]
            / params[0]["Nominal cell capacity [A.h]"],
            2
        )
        temp = round(params[0]["Ambient temperature [K]"] - 273.15, 2)

        if param_to_vary is None and is_comparison:
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
        elif param_to_vary is not None and is_comparison:
            if param_to_vary == "Current function [A]":
                tweet_text = (
                    f"{model[0].name} with {chemistry['citation']} parameters "
                    f"varying '{param_to_vary}' at {temp}°C"
                )
            elif param_to_vary == "Ambient temperature [K]":
                tweet_text = (
                    f"{model[0].name} with {chemistry['citation']} parameters "
                    f"varying '{param_to_vary}' for a {c_rate} C discharge"
                )
            else:
                tweet_text = (
                    f"{model[0].name} with {chemistry['citation']} parameters "
                    f"varying '{param_to_vary}' for a {c_rate} C discharge at "
                    f"{temp}°C"
                )

    if len(tweet_text + " https://bit.ly/3z5p7q9") > 280:
        tweet_text = tweet_text.split(":")[0]
        tweet_text += " \U0001F53D"
        experiment = f"{cycle} * {number}"
    else:
        experiment = None

    return tweet_text + " https://bit.ly/3z5p7q9", experiment
