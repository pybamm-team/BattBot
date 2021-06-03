import tweepy
import matplotlib.pyplot as plt
import os
from plotting.random_plot_generator import random_plot_generator
from information.information import information
import multiprocessing
# import time


def tweet_graph(testing=False):
    """
    Function responsible for all the tweeting functionalities.
    Parameters:
        testing: bool
            default: False
    """

    # getting the Twitter API keys
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_KEY = os.environ["ACCESS_KEY"]
    ACCESS_SECRET = os.environ["ACCESS_SECRET"]

    # setting up tweepy.API object
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    (
        model,
        parameter_values,
        time,
        chemistry,
        solver,
        is_experiment,
        cycle,
        number,
        is_comparison,
    ) = random_plot_generator(
        testing=testing,
        provided_choice=0
    )

    tweet = (
        information(
            chemistry,
            model,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison
        )
        + ", at time = "
        + str(time)
        + " s"
    )

    print(tweet)
    # Uncomment to tweet
    media = api.media_upload("plot.gif")

    if not testing:
        api.update_status(status=tweet, media_ids=[media.media_id])

    os.remove("plot.gif")
    plt.clf()


# uncomment when simulating tweeting process
# while True:
#     tweet_graph()
#     time.sleep(5)

# Uncomment when running on schedule
if __name__ == "__main__":  # pragma: no cover

    while True:

        tweet = multiprocessing.Process(target=tweet_graph)
        tweet.start()
        tweet.join(900)

        if tweet.is_alive():

            print(
                "The simulation is taking longer than expected, KILLING IT"
                + " and starting a NEW ONE."
            )
            tweet.kill()
            tweet.join()

        else:
            break
