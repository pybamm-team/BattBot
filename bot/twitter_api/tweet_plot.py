import datetime
import multiprocessing
import os
import random
import time

import matplotlib.pyplot as plt

from plotting.random_plot_generator import random_plot_generator
from twitter_api.upload import Upload
from utils.custom_process import Process
from utils.tweet_text_generator import tweet_text_generator


class Tweet(Upload):
    """
    Tweets a random battery simulation.

    Parameter
    ---------
        testing : bool
            To be used while testing.
        choice : str
            To be used while testing. Can be "model comparison",
            "parameter comparison" or "degradation comparison
            (summary variables)".
    """

    def __init__(self, testing=False, choice=None):
        """
        Defines video tweet properties
        """
        super().__init__()
        # create a random GIF
        while True:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            choice_list = [
                "degradation comparison",
                "model comparison",
                "parameter comparison",
            ]
            if choice is None:
                choice = random.choice(choice_list)

            p = Process(
                target=random_plot_generator, args=(return_dict, choice, None, testing)
            )

            p.start()
            # time-out
            p.join(1200)

            if p.is_alive():  # pragma: no cover
                print(
                    "Simulation is taking too long,",
                    "KILLING IT and starting a NEW ONE.",
                )
                p.kill()
                p.join()
            else:  # pragma: no cover
                break

        if os.path.exists("plot.gif"):
            self.plot = "plot.gif"
        elif os.path.exists("plot.png"):
            self.plot = "plot.png"
        self.total_bytes = os.path.getsize(self.plot)
        self.config = None
        self.model = return_dict["model"]
        self.chemistry = return_dict["chemistry"]
        self.is_experiment = return_dict["is_experiment"]
        self.cycle = return_dict["cycle"]
        self.number = return_dict["number"]
        self.is_comparison = return_dict["is_comparison"]
        self.param_to_vary = return_dict["param_to_vary"]
        self.varied_values = return_dict["varied_values"]
        self.params = (
            return_dict["params"]
            if choice == "model comparison" or choice == "parameter comparison"
            else None
        )
        self.degradation_mode = (
            return_dict["degradation_mode"]
            if "degradation_mode" in return_dict
            else None
        )
        self.degradation_value = (
            return_dict["degradation_value"]
            if "degradation_value" in return_dict
            else None
        )
        self.testing = testing

    def write_config(self, filename, append=False):  # pragma: no cover
        """
        Writes the random config to config.txt and appends the same to
        data.txt with date and time.

        Parameters
        ----------
            filename : str
                Name of the file to write to.
            append : bool
                default: False
                If the file has to be opened up in append mode.
        """
        # the configuration for the GIF
        self.config = {
            "model": str(self.model),
            "model options": self.model.options
            if not isinstance(self.model, dict)
            else None,
            "chemistry": self.chemistry,
            "is_experiment": self.is_experiment,
            "cycle": self.cycle,
            "number": self.number,
            "is_comparison": self.is_comparison,
            "param_to_vary": self.param_to_vary,
            "varied_values": self.varied_values,
        }

        # append to data.txt and write to config.txt
        if not append:
            with open(filename, "w") as f:
                f.write(str(self.config))
        elif append:
            with open(filename, "a") as f:
                f.write(
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    + " "
                    + str(self.config)
                    + "\n"
                )

    def tweet(self):
        """
        Publishes Tweet with attached plot
        """
        # generate a text for the tweet
        tweet_status, experiment = tweet_text_generator(
            self.chemistry,
            self.model,
            self.is_experiment,
            self.cycle,
            self.number,
            self.is_comparison,
            self.param_to_vary,
            self.params,
            self.degradation_mode,
            self.degradation_value,
        )

        # data for the GIF tweet
        request_data = {"status": tweet_status, "media_ids": self.media_id}

        if not self.testing:
            # tweet the GIF
            req = self.post_request(self.post_tweet_url, request_data, self.oauth)

            # write the config in txt files for users to reproduce
            self.write_config("config.txt")
            self.write_config("data.txt", append=True)

            # reply to the posted tweet
            if experiment is not None:  # pragma: no cover
                reply = {
                    "status": experiment,
                    "in_reply_to_status_id": req.json()["id"],
                    "auto_populate_reply_metadata": True,
                }

                # post reply
                self.post_request(self.post_tweet_url, reply, self.oauth)

        if os.path.exists("plot.gif"):
            os.remove("plot.gif")
        if os.path.exists("plot.png"):
            os.remove("plot.png")
        plt.close()


if __name__ == "__main__":
    tweet = Tweet()
    tweet.upload_init()
    tweet.upload_append()
    tweet.upload_finalize()
    if not tweet.testing:
        time.sleep(random.randint(0, 3600))
    tweet.tweet()
