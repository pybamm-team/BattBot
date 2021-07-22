import time
import tweepy
from api_keys import Keys


# setting up the API keys, tweepy auth and tweepy api object
keys = Keys()
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# inspired from https://www.youtube.com/watch?v=W0wWwglE1Vc
class Reply:

    def __init__(self, testing=False):
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

    def reply_to_tweet(self):
        """
        Replies to a tweet where the bot was mentioned with the
        hashtag "battbot".
        """
        if self.testing:
            last_seen_id = self.retrieve_tweet_id("bot/last_seen_id.txt")
        else:   # pragma: no cover
            last_seen_id = self.retrieve_tweet_id("last_seen_id.txt")

        # retreiving all the mentions after the tweet with id=last_seen_id
        mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

        # iterating through all the mentions if not testing
        if not self.testing:    # pragma: no cover
            for mention in reversed(mentions):
                # storing the id
                self.store_tweet_id(mention._json["id"], "last_seen_id.txt")
                print(
                    mention.user.screen_name + " "
                    + mention.full_text + " "
                    + str(mention._json["id"])
                )

                # reading the tweet text
                if '#battbot' in mention.full_text.lower():

                    # replying
                    api.update_status(
                        "@"
                        + mention.user.screen_name
                        + " Hi there! The replying feature is still under "
                        + "active development. "
                        + "Try this again in a few weeks :)",
                        mention._json["id"]
                    )


if __name__ == "__main__":  # pragma: no cover
    reply = Reply()
    while True:
        reply.reply_to_tweet()
        time.sleep(60)
