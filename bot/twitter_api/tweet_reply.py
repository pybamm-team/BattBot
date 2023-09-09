import os
import time

import matplotlib.pyplot as plt
import pybamm
from PIL import Image

from plotting.random_plot_generator import random_plot_generator
from twitter_api.upload import Upload
from utils.custom_process import Process


# basic structure inspired from - https://www.youtube.com/watch?v=W0wWwglE1Vc
class Reply(Upload):
    """
    Replies to a tweet in which the bot is tagged.

    Parameters
    ----------
        testing : bool
            To be used while testing, so that the function doesn't reply.
    """

    def __init__(self, testing=False):
        super().__init__()
        self.testing = testing

    def retrieve_tweet_id(self, file_name):
        """
        Returns the id of the tweet (in which the bot was mentioned)
        last seen by the bot.

        Parameters
        ----------
            file_name : str
                Path of the file where the `last_seen_id` is stored.
        """
        with open(file_name) as f:
            last_seen_id = int(f.read().strip())
        return last_seen_id

    def store_tweet_id(self, last_seen_id, file_name):
        """
        Store the id of a tweet (in which the bot was mentioned)
        in a text file.

        Parameters
        ----------
            last_seen_id : numerical
                ID of tweet last seen by the bot.
            file_name : str
                Path of the file where the `last_seen_id` has to be stored.
        """
        with open(file_name, "w") as f:
            f.write(str(last_seen_id))

    def generate_reply(self, tweet_text, testing=False):
        """
        Generates an appropriate GIF for the given tweet text.

        Parameters
        ----------
            tweet_text : str
                Text extracted from the tweet.
        """
        request_examples = (
            "https://github.com/pybamm-team/BattBot/blob/main/REQUEST_EXAMPLES.md"
        )
        models = []
        reply_config = {}

        # split the tweet text and remove all ','
        text_list = (
            tweet_text.lower()
            .replace(",", " ")
            .replace(":", " ")
            .replace("-", " ")
            .split(" ")
        )
        text_list = [x for x in text_list if x != ""]

        # check if there are 2 occurrences of "single"
        single_indices = [
            i for i, x in enumerate(text_list) if x == "single" or "spm" in x
        ]

        if "compare" not in text_list and "vary" not in text_list:
            raise Exception(
                "I'm sorry, I couldn't understand the requested simulation.",
                f"Some tweet examples - {request_examples}",
            )

        # if there are, append SPM and SPMe to models
        if len(single_indices) > 1:
            models.append(pybamm.lithium_ion.SPM())
            models.append(pybamm.lithium_ion.SPMe())
        # if user wants "SPM"
        elif (
            "single" in text_list
            and "particle" in text_list
            and "electrolyte" not in text_list
        ) or "spm" in text_list:
            models.append(pybamm.lithium_ion.SPM())
        # if user wants "SPMe"
        elif (
            "single" in text_list
            and "particle" in text_list
            and "electrolyte" in text_list
        ) or "spme" in text_list:
            models.append(pybamm.lithium_ion.SPMe())
        # if user wants "DFN" model
        if "doyle-fuller-newman" in text_list or "dfn" in text_list:
            models.append(pybamm.lithium_ion.DFN())

        # if less than 2 models are provided for "model comparison"
        # or no model is provided for "parameter comparison"
        if len(models) <= 1 and "compare" in text_list:
            raise Exception(
                "Please provide at least 2 models. Some tweet examples -",
                f"{request_examples}",
            )
        elif len(models) != 1 and "vary" in text_list:
            raise Exception(
                "Please provide a model. Some tweet examples - " + f"{request_examples}"
            )

        models_for_comp = dict(list(enumerate(models)))

        if "chen2020" in text_list:
            chemistry = "Chen2020"
        elif "marquis2019" in text_list:
            chemistry = "Marquis2019"
        elif "ai2020" in text_list:
            chemistry = "Ai2020"
        else:
            # if no chemistry is provided
            raise Exception(
                "Please provide a parameter set in the format - Chen2020.",
                f"Some tweet examples - {request_examples}",
            )

        # parameter values
        params = pybamm.ParameterValues(chemistry)

        # update "Ambient temperature [K]" from the tweet text
        temp_is_present = False
        try:
            for x in text_list:
                if x[-1] == "k" and len(x) > 1:
                    params["Ambient temperature [K]"] = float(x[:-1])
                    temp_is_present = True
                    break
        except Exception:
            raise Exception(
                "Please provide 'Ambient temperature' in the format -",
                f"273.15K. Some tweet examples - {request_examples}",
            )
        finally:
            if not temp_is_present:
                raise Exception(
                    "Please provide 'Ambient temperature' in the format - "
                    + f"273.15K. Some tweet examples - {request_examples}"
                )

        # update "Current function [A]" from the tweet text
        if "experiment" not in text_list:
            c_rate_is_present = False
            try:
                for x in text_list:
                    if x[-1] == "c" and len(x) > 1:
                        c_rate = float(x[:-1])
                        c_rate_is_present = True
                        params["Current function [A]"] = (
                            c_rate
                            * pybamm.ParameterValues(chemistry)[
                                "Nominal cell capacity [A.h]"
                            ]
                        )
                        break
            except Exception:
                raise Exception(
                    "Please provide 'C rate' in the format - "
                    + f"1C. Some tweet examples - {request_examples}"
                )
            finally:
                if not c_rate_is_present:
                    raise Exception(
                        "Please provide 'C rate' in the format - "
                        + f"1C. Some tweet examples - {request_examples}"
                    )

        # read the provided experiment
        if "experiment" in text_list and "vary" not in text_list:
            is_experiment = True
            try:
                cycle = eval(  # noqa: PGH001
                    tweet_text[tweet_text.index("[") : tweet_text.index("]") + 1]
                )
                number = int(tweet_text[tweet_text.index("*") + 2])
                pybamm.Experiment(cycle * number)
            except Exception:
                raise Exception(
                    "Please provide experiment in the format - "
                    + "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2."  # noqa: E501
                    + f" Some tweet examples - {request_examples}",
                )
        # having varied values in the text makes the process of extraction of experiment
        # a bit tricky -
        # "Electrode height [m]" with values [x, y, z] with experiment [(a), (b), (c)]
        # so the script starts looking for "[" and "]" from the end
        elif "experiment" in text_list and "vary" in text_list:
            is_experiment = True
            try:
                cycle = eval(  # noqa: PGH001
                    tweet_text[tweet_text.rindex("[") : tweet_text.rindex("]") + 1]
                )
                number = int(tweet_text[tweet_text.index("*") + 2])
                pybamm.Experiment(cycle * number)
            except Exception:
                raise Exception(
                    "Please provide experiment in the format - "
                    + "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2."  # noqa: E501
                    + f" Some tweet examples - {request_examples}",
                )
        else:
            is_experiment = False
            cycle = None
            number = None

        # if "model comparison"
        if "compare" in text_list:
            choice = "model comparison"

            reply_config.update(
                {
                    "varied_values_override": None,
                    "param_to_vary_info": None,
                    "params": params,
                }
            )
        elif "vary" in text_list:
            choice = "parameter comparison"

            try:
                # extract the varied parameter
                param_to_vary = tweet_text[
                    tweet_text.index('"') : tweet_text.index(
                        '"', tweet_text.index('"') + 1
                    )
                    + 1
                ].replace('"', "")
                params[param_to_vary]

                # extract the varied values
                # if an experiment is provided
                if is_experiment:
                    # if the varied parameter has units / dimensions
                    if tweet_text.count("]") > 2:
                        varied_values = eval(  # noqa: PGH001
                            tweet_text[
                                tweet_text.index(
                                    "[", tweet_text.index("]") + 1
                                ) : tweet_text.index("]", tweet_text.index("]") + 1)
                                + 1
                            ]
                        )
                    # if the varied parameter does not have units / dimensions
                    elif tweet_text.count("]") == 2:
                        varied_values = eval(  # noqa: PGH001
                            tweet_text[
                                tweet_text.index("[") : tweet_text.index("]") + 1
                            ]
                        )
                else:
                    varied_values = eval(  # noqa: PGH001
                        tweet_text[tweet_text.rindex("[") : tweet_text.rindex("]") + 1]
                    )

                reply_config.update(
                    {
                        "varied_values_override": varied_values,
                        "param_to_vary_info": {
                            param_to_vary: {"print_name": None, "bounds": (None, None)}
                        },
                    }
                )
            except Exception:
                raise Exception(
                    "Please provide a parameter to vary and the varied values in the "
                    + 'format - "Parameter to vary" with the values [1, 2, 3]. '
                    + f"Some tweet examples - {request_examples}"
                )

        reply_config.update(
            {
                "chemistry": chemistry,
                "models_for_comp": models_for_comp,
                "is_experiment": is_experiment,
                "cycle": cycle,
                "number": number,
                "params": params,
            }
        )

        # generate the simulation and GIF
        return_dict = {}
        random_plot_generator(
            return_dict, choice, reply_config=reply_config, testing=testing
        )

    def reply(self):
        """
        Replies to a tweet where the bot was mentioned with the
        hashtag "battbot".
        """
        if self.testing:
            last_seen_id = self.retrieve_tweet_id("bot/last_seen_id.txt")
        else:  # pragma: no cover
            last_seen_id = self.retrieve_tweet_id("last_seen_id.txt")

        # retrieving all the mentions after the tweet with id=last_seen_id
        mentions = self.api.mentions_timeline(
            since_id=last_seen_id, tweet_mode="extended"
        )

        # iterating through all the mentions if not testing
        if not self.testing:
            for mention in reversed(mentions):
                # storing the id
                self.store_tweet_id(mention._json["id"], "last_seen_id.txt")

                # reading the tweet text
                if "#battbot" in mention.full_text.lower():
                    print(
                        mention.user.screen_name
                        + " "
                        + mention.full_text
                        + " "
                        + str(mention._json["id"])
                    )
                    tweet_text = mention.full_text

                    # creating a custom process to generate the requested simulation
                    p = Process(target=self.generate_reply, args=(tweet_text,))

                    p.start()
                    # time-out
                    p.join(1200)

                    # if the process is alive after 10 minutes
                    if p.is_alive():  # pragma: no cover
                        self.api.update_status(
                            "@"
                            + mention.user.screen_name
                            + " Hi there! The simulation took more than "
                            + "20 minutes and hence, it was cancelled."
                            + "Please try again with a simpler simulation "
                            + "(this feature is still in the testing phase).",
                            mention._json["id"],
                        )

                        p.kill()
                        p.join()
                        return

                    # if there was an Exception in the process
                    if p.exception:
                        e, traceback = p.exception
                        self.api.update_status(
                            "@" + mention.user.screen_name + f" {e}",
                            mention._json["id"],
                        )

                        p.kill()
                        p.join()
                        return

                    # finding the file which has to be tweeted
                    if os.path.exists("plot.gif"):
                        self.plot = "plot.gif"
                    elif os.path.exists("plot.png"):
                        self.plot = "plot.png"
                    self.total_bytes = os.path.getsize(self.plot)

                    # initiate the upload
                    self.upload_init()
                    # append the chunks
                    self.upload_append()
                    # finalize upload
                    self.upload_finalize()

                    # reply configuration
                    img = Image.open("plot.gif").size
                    if img[0] <= 1080:  # pragma: no cover
                        status = (
                            "This GIF has been compressed twice, to bring its size down to 15 MB (twitter's limit). "  # noqa: E501
                            + "Please request a smaller simulation for a better quality GIF."  # noqa: E501
                        )
                    else:
                        status = None
                    reply = {
                        "status": status,
                        "in_reply_to_status_id": mention._json["id"],
                        "auto_populate_reply_metadata": True,
                        "media_ids": self.media_id,
                    }

                    # post the reply
                    self.post_request(self.post_tweet_url, reply, self.oauth)

                    if os.path.exists("plot.gif"):
                        os.remove("plot.gif")
                    if os.path.exists("plot.png"):
                        os.remove("plot.png")
                    plt.close()


if __name__ == "__main__":
    reply = Reply()
    while True:
        reply.reply()
        time.sleep(60)
