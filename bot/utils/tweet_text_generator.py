def tweet_text_generator(
    chemistry,
    model,
    is_experiment,
    cycle,
    number,
    is_comparison,
    param_to_vary,
    params,
    degradation_mode,
    degradation_value,
):
    """
    Generates tweet text.

    Parameters
    ----------
        chemistry : dict
        model : :class:`pybamm.BaseBatteryModel` or dict
        is_experiment : bool
        cycle : list or None
        number : numerical or None
        is_comparison : bool
        param_to_vary : str or None
        params : dict
            To be used when varied values have to be added to the tweet text.
        degradation_mode : str or None
        degradation_value : str or None

    Returns
    -------
        tweet_text : str
        experiment : str or None
            Not none if the tweet text exceeds twitter limit.
    """

    if is_comparison:
        # calculate C-rate and Temperature to add in tweet text
        c_rate = round(
            params[0]["Current function [A]"]
            / params[0]["Nominal cell capacity [A.h]"],
            2,
        )
        temp = round(params[0]["Ambient temperature [K]"] - 273.15, 2)

    # summary variable
    if is_experiment and not is_comparison:
        tweet_text = (
            f"Plotting {model.name} with {chemistry['citation']} "
            f"parameters and {degradation_value} {degradation_mode} "
            f"for the following experiment: {cycle} * {number}"
        )

    # simulating an experiment
    elif is_experiment:
        # comparing a single experiment with different models
        if param_to_vary is None and is_comparison:
            if len(model) == 2:
                tweet_text = (
                    f"Comparing {model[0].name} and {model[1].name} "
                    f"with {chemistry['citation']} parameters at {temp}°C for the "
                    f"following experiment: {cycle} * {number}"
                )
            else:
                tweet_text = (
                    f"Comparing {model[0].name}, {model[1].name}, and "
                    f"{model[2].name} with {chemistry['citation']} "
                    f"parameters at {temp}°C for the following experiment: "
                    f"{cycle} * {number}"
                )
        # comparing a single model and a single experiment while varying
        # a parameter
        elif param_to_vary is not None and is_comparison:
            tweet_text = (
                f"{model[0].name} with {chemistry['citation']} parameters "
                f"varying '{param_to_vary}' at {temp}°C for the following experiment: "
                f"{cycle} * {number}"
            )

    # not simulating an experiment
    elif not is_experiment:

        # comparing 2 or more models with a constant discharge
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

        # comparing a single model by varying a parameter value
        elif param_to_vary is not None and is_comparison:
            tweet_text = (
                f"{model[0].name} with {chemistry['citation']} parameters "
                f"varying '{param_to_vary}' for a {c_rate} C discharge at "
                f"{temp}°C"
            )

    # if txt is greater the=an twitter limit, create a tweet
    # thread and add the experiment in a reply
    if len(tweet_text + " https://bit.ly/3z5p7q9") > 280:
        tweet_text = tweet_text.split(":")[0]
        tweet_text += " \U0001F53D"
        experiment = f"{cycle} * {number}"
    else:
        experiment = None

    return tweet_text + " https://bit.ly/3z5p7q9", experiment
