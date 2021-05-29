import tweepy
import matplotlib.pyplot as plt
import os
from plotting.random_plot_generator import random_plot_generator
from information.information import information


def tweet_graph(testing=None):

    # getting the Twitter API keys
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_KEY = os.environ["ACCESS_KEY"]
    ACCESS_SECRET = os.environ["ACCESS_SECRET"]

    # setting up tweepy.API object
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    if not testing:
        (
            model,
            parameter_values,
            time,
            chemistry,
            solver,
            isExperiment,
            cycle,
            number,
            isComparison,
        ) = random_plot_generator()

        tweet = (
            information(
                chemistry,
                model,
                solver,
                isExperiment,
                cycle,
                number,
                isComparison
            )
            + ", at time = "
            + str(time)
            + " s"
        )

        print(tweet)
    # Uncomment to tweet
    media = api.media_upload("plot.png")

    if not testing:
        api.update_status(status=tweet, media_ids=[media.media_id])

    os.remove("plot.png")
    plt.clf()


# uncomment when simulating tweeting process
# while True:
#     tweet_graph()
#     time.sleep(5)

# Uncomment when running on schedule
if __name__ == "__main__":
    tweet_graph()
