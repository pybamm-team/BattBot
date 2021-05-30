def information(
    chemistry,
    model,
    solver,
    isExperiment,
    cycle,
    number,
    isComparison
):
    """
    Generates tweet text.
    Parameters:
        chemistry: dict
        model: pybamm.BaseModel
        solver: pybamm.BaseSolver
        isExperiment: bool
        cycle: list
        number: numerical
        isComparison: bool
    Returns
        tweet_text: str
    """

    if isExperiment:
        tweet_text = (
            str(cycle)
            + " * "
            + str(number)
            + " "
            + str(model)
            + " "
            + str(chemistry["citation"])
        )
        return tweet_text

    elif isComparison:
        tweet_text = str(model)
        return tweet_text
    else:
        tweet_text = (
            str(model) + " " + str(chemistry["citation"]) + " " + str(solver)
        )
        return tweet_text
