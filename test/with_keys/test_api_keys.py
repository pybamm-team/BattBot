import tweepy
import unittest
from bot.twitter_api.api_keys import Keys


class TestApiKeys(unittest.TestCase):
    def test_api_keys(self):

        keys = Keys()

        ACCESS_TOKEN = keys.ACCESS_TOKEN
        ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
        CONSUMER_KEY = keys.CONSUMER_KEY
        CONSUMER_SECRET = keys.CONSUMER_SECRET

        self.assertIsInstance(ACCESS_TOKEN, str)
        self.assertIsInstance(ACCESS_TOKEN_SECRET, str)
        self.assertIsInstance(CONSUMER_KEY, str)
        self.assertIsInstance(CONSUMER_SECRET, str)

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        self.assertTrue(api.verify_credentials())
