import os
import tweepy


class Keys:

    def __init__(self):
        self.CONSUMER_KEY = os.environ["CONSUMER_KEY"]
        self.CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
        self.ACCESS_TOKEN = os.environ["ACCESS_KEY"]
        self.ACCESS_TOKEN_SECRET = os.environ["ACCESS_SECRET"]
        self.auth = tweepy.OAuthHandler(
            self.CONSUMER_KEY, self.CONSUMER_SECRET
        )
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
