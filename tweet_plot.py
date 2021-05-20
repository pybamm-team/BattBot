import pybamm
import tweepy
import time
import matplotlib.pyplot as plt
import importlib.util
import os
from plotting.random_plot_generator import random_plot_generator
from information.information import information


# getting the Twitter API keys
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = ""

# setting up tweepy.API object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def tweet_graph():

    print("Tweeting")
    (   
        model,
        parameter_values,
        time_of_png,
        parameter_number,
    ) = random_plot_generator()

    tweet = (
        information(parameter_number, model)
        + ", at time = "
        + str(time_of_png)
        + " s"
    )

    print(tweet)
    # Uncomment to tweet
    # media = api.media_upload("plot.png")

    # api.update_status(status=tweet, media_ids=[media.media_id])
    api.update_status(status=tweet)

    os.remove("plot.png")
    # plt.clf()
    print("Tweeted")

# Simulate tweeting process
# while True:
#     tweet_graph()
#     time.sleep(30)

# Uncomment when running on schedule
tweet_graph()