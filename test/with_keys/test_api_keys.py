import unittest

import tweepy
from bot.twitter_api.api_keys import Keys


class TestApiKeys(unittest.TestCase):
    def test_api_keys(self):
        keys = Keys()

        ACCESS_TOKEN = keys.ACCESS_TOKEN
        ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
        CONSUMER_KEY = keys.CONSUMER_KEY
        CONSUMER_SECRET = keys.CONSUMER_SECRET

        assert isinstance(ACCESS_TOKEN, str)
        assert isinstance(ACCESS_TOKEN_SECRET, str)
        assert isinstance(CONSUMER_KEY, str)
        assert isinstance(CONSUMER_SECRET, str)

        auth = tweepy.OAuth1UserHandler(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET,
        )

        api = tweepy.API(auth)

        assert api.verify_credentials()


if __name__ == "__main__":
    unittest.main()
