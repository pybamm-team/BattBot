def information(
    chemistry,
    model,
    is_experiment,
    cycle,
    number,
    is_comparison
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
    Returns
        tweet_text: str
    """

    if is_experiment:
        tweet_text = (
            str(cycle)
            + " * "
            + str(number)
            + " "
            + str(model.name)
            + " "
            + str(chemistry["citation"])
        )
        return tweet_text

    elif is_comparison:
        tweet_text = str(chemistry["citation"])
        return tweet_text
    else:
        tweet_text = (
            str(model.name)
            + " "
            + str(chemistry["citation"])
        )
        return tweet_text
