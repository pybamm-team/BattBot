import re
import time
import pybamm
import multiprocessing
from twitter_api.upload import Upload
from plotting.random_plot_generator import random_plot_generator


# inspired from https://www.youtube.com/watch?v=W0wWwglE1Vc
class Reply(Upload):
    def __init__(self, testing=False):
        super().__init__()
        self.testing = testing

    def retrieve_tweet_id(self, file_name):
        """
        Returns the id of the tweet (in which the bot was mentioned)
        last seen by the bot.
        """
        f = open(file_name, "r")
        last_seen_id = int(f.read().strip())
        f.close()
        return last_seen_id

    def store_tweet_id(self, last_seen_id, file_name):
        """
        Store the id of a tweet (in which the bot was mentioned)
        in a text file.
        """
        f = open(file_name, "w")
        f.write(str(last_seen_id))
        f.close()
        return

    def generate_config(self, tweet_text):
        models = []
        reply_config = {}
        text_list = tweet_text.split(" ")
        if (
            re.search(r"\bsingle particle model\b", tweet_text)
            and "electrolyte" not in text_list
        ) or re.search(r"\bspm\b", tweet_text):
            models.append(pybamm.lithium_ion.SPM())
        if "doyle-fuller-newman" in tweet_text or "dfn" in tweet_text:
            models.append(pybamm.lithium_ion.DFN())
        if (
            "single particle model woth electrolyte" in tweet_text
            or "spme" in tweet_text
        ):
            models.append(pybamm.lithium_ion.SPMe())

        models_for_comp = dict(list(enumerate(models)))

        if "compare" in tweet_text:

            choice = "model comparison"

            chemistry = text_list[text_list.index("parameters") - 1]

            if chemistry == "chen2020":
                chemistry = pybamm.parameter_sets.Chen2020

            reply_config.update(
                {
                    "chemistry": chemistry,
                    "models_for_comp": models_for_comp,
                    "is_experiment": False,
                    "cycle": None,
                    "number": None,
                    "param_to_vary": None,
                    "bounds": None,
                }
            )

        return reply_config, choice

    def reply_to_tweet(self):
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
        if not self.testing:  # pragma: no cover
            for mention in reversed(mentions):
                # storing the id
                self.store_tweet_id(mention._json["id"], "last_seen_id.txt")

                models = []
                # reading the tweet text
                if "#battbot" in mention.full_text.lower():

                    print(
                        mention.user.screen_name
                        + " "
                        + mention.full_text
                        + " "
                        + str(mention._json["id"])
                    )

                    try:
                        reply_config, choice = self.generate_config(
                            mention.full_text.lower()
                        )

                        manager = multiprocessing.Manager()
                        return_dict = manager.dict()

                    
                        p = multiprocessing.Process(
                            target=random_plot_generator,
                            args=(return_dict, choice, reply_config),
                        )

                        p.start()
                        # time-out
                        p.join(600)

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
                    except Exception as e:
                        pass
                        # self.api.update_status(
                        #     "@"
                        #     + mention.user.screen_name
                        #     + " Hi there! There was an error while solving the "
                        #     + f"simulation - {e}. "
                        #     + "Please try again with a different configuration.",
                        #     mention._json["id"],
                        # )

                        return

                    # replying
                    self.api.update_status(
                        "@"
                        + mention.user.screen_name
                        + " Hi there! The replying feature is still under "
                        + "active development. "
                        + "Try this again in a few weeks :)",
                        mention._json["id"],
                    )


if __name__ == "__main__":  # pragma: no cover
    reply = Reply()
    while True:
        reply.reply_to_tweet()
        time.sleep(60)
