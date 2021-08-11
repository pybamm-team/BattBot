import os
import time
import pybamm
import matplotlib.pyplot as plt
from twitter_api.upload import Upload
from utils.custom_process import Process
from plotting.random_plot_generator import random_plot_generator


# basic structure inspired from - https://www.youtube.com/watch?v=W0wWwglE1Vc
class Reply(Upload):
    """
    Replies to a tweet in which the bot is tagged.
    Parameters:
        testing: bool
    """

    def __init__(self, testing=False):
        super().__init__()
        self.testing = testing

    def retrieve_tweet_id(self, file_name):
        """
        Returns the id of the tweet (in which the bot was mentioned)
        last seen by the bot.
        Parameters:
            file_name: str
        """
        f = open(file_name, "r")
        last_seen_id = int(f.read().strip())
        f.close()
        return last_seen_id

    def store_tweet_id(self, last_seen_id, file_name):
        """
        Store the id of a tweet (in which the bot was mentioned)
        in a text file.
        Parameters:
            last_seen_id: numerical
            file_name: str
        """
        f = open(file_name, "w")
        f.write(str(last_seen_id))
        f.close()

    def generate_reply(self, tweet_text):
        """
        Generates an appropriate GIF fot the given tweet text.
        Parameters:
            tweet_text: str
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

        # check if there are 2 occurences of "single"
        single_indices = [
            i for i, x in enumerate(text_list) if x == "single" or "spm" in x
        ]

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
                "Please provide atleast 2 models. Some tweet examples - "
                + f"{request_examples}"
            )
        elif len(models) == 0:
            raise Exception(
                "Please provide atleast 1 model. Some tweet examples - "
                + f"{request_examples}"
            )

        models_for_comp = dict(list(enumerate(models)))

        if "chen2020" in text_list:
            chemistry = pybamm.parameter_sets.Chen2020
        elif "marquis2019" in text_list:
            chemistry = pybamm.parameter_sets.Marquis2019
        elif "ai2020" in text_list:
            chemistry = pybamm.parameter_sets.Ai2020
        else:
            # if no chemistry is provided
            raise Exception(
                "Please provide a parameter set in the format - Chen2020. "
                + f"Some tweet examples - {request_examples}"
            )

        # parameter values
        params = pybamm.ParameterValues(chemistry=chemistry)

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
                "Please provide 'Ambient temperature' in the format - "
                + f"273.15K. Some tweet examples - {request_examples}"
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
                            * pybamm.ParameterValues(chemistry=chemistry)[
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
        if "experiment" in text_list:
            is_experiment = True
            current = None
            try:
                cycle = eval(
                    tweet_text[tweet_text.index("[") : tweet_text.index("]") + 1]
                )
                number = int(tweet_text[tweet_text.index("*") + 2])
                pybamm.Experiment(cycle * number)
            except Exception:
                raise Exception(
                    "Please provide experiment in the format - "
                    + "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2."  # noqa
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
                    "chemistry": chemistry,
                    "models_for_comp": models_for_comp,
                    "is_experiment": is_experiment,
                    "cycle": cycle,
                    "number": number,
                    "param_to_vary_info": None,
                    "params": params
                }
            )

        else:
            raise Exception(
                "I'm sorry, I couldn't understand the requested simulation. "
                + f"Some tweet examples - {request_examples}"
            )

        # generate the simulation and GIF
        return_dict = {}
        random_plot_generator(return_dict, choice, reply_config=reply_config)

    def reply(self):
        """
        Replies to a tweet where the bot was mentioned with the
        hashtag "battbot".
        """
        if self.testing:
            last_seen_id = self.retrieve_tweet_id("bot/last_seen_id.txt")
        else:  # pragma: no cover
            last_seen_id = self.retrieve_tweet_id("last_seen_id.txt")

        # retreiving all the mentions after the tweet with id=last_seen_id
        mentions = self.api.mentions_timeline(last_seen_id, tweet_mode="extended")

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
                    p.join(600)

                    # if the process is alive after 10 minutes
                    if p.is_alive():  # pragma: no cover
                        self.api.update_status(
                            "@"
                            + mention.user.screen_name
                            + " Hi there! The simulation took more than "
                            + "10 minutes and hence, it was cancelled."
                            + "Please try again with a simpler simulation ",
                            +"(this feature is still in the testing phase).",
                            mention._json["id"],
                        )

                        return

                    # if there was an Exception in the process
                    if p.exception:
                        e, traceback = p.exception
                        self.api.update_status(
                            "@" + mention.user.screen_name + f" {e}",
                            mention._json["id"],
                        )

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
                    # finalize uplaod
                    self.upload_finalize()

                    # reply configuration
                    reply = {
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
