import os
import unittest

import pybamm
from bot.twitter_api.tweet_plot import Tweet


class TestTweet(unittest.TestCase):
    def test_tweet(self):
        tweet = Tweet(testing=True, choice="degradation comparison")

        assert tweet.media_id is None
        assert isinstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        assert tweet.processing_info is None
        assert isinstance(tweet.model, pybamm.BaseModel)
        assert isinstance(tweet.chemistry, str)
        assert isinstance(tweet.is_experiment, bool)
        assert tweet.is_experiment
        assert isinstance(tweet.cycle, list)
        assert isinstance(tweet.cycle[0], tuple)
        assert isinstance(tweet.number, int)
        assert isinstance(tweet.is_comparison, bool)
        assert not tweet.is_comparison
        assert isinstance(tweet.testing, bool)
        assert isinstance(tweet.param_to_vary, str)
        assert isinstance(tweet.varied_values, list)
        assert tweet.params is None
        assert isinstance(tweet.degradation_mode, str)
        assert isinstance(tweet.degradation_value, str)

        tweet.upload_init()

        assert tweet.media_id is not None

        tweet.upload_append()
        tweet.upload_finalize()
        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True, choice="model comparison")

        assert tweet.media_id is None
        assert isinstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        assert tweet.processing_info is None
        assert isinstance(tweet.model, dict)
        assert isinstance(tweet.chemistry, str)
        assert isinstance(tweet.is_experiment, bool)
        assert isinstance(tweet.is_comparison, bool)
        assert tweet.is_comparison
        assert isinstance(tweet.testing, bool)
        assert isinstance(tweet.varied_values, dict)
        assert isinstance(tweet.params, dict)
        assert tweet.degradation_mode is None, None
        assert tweet.degradation_value is None, None

        tweet.upload_init()

        assert tweet.media_id is not None

        tweet.upload_append()
        tweet.upload_finalize()

        assert tweet.processing_info is not None

        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True, choice="parameter comparison")

        assert tweet.media_id is None
        assert isinstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        assert tweet.processing_info is None
        assert isinstance(tweet.model, dict)
        assert isinstance(tweet.chemistry, str)
        assert isinstance(tweet.is_experiment, bool)
        assert isinstance(tweet.is_comparison, bool)
        assert tweet.is_comparison
        assert isinstance(tweet.testing, bool)
        assert isinstance(tweet.varied_values, list)
        assert isinstance(tweet.params, dict)
        assert tweet.degradation_mode is None, None
        assert tweet.degradation_value is None, None

        tweet.upload_init()

        assert tweet.media_id is not None

        tweet.upload_append()
        tweet.upload_finalize()

        assert tweet.processing_info is not None

        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True)

        assert tweet.media_id is None
        assert isinstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        assert tweet.processing_info is None
        assert isinstance(tweet.model, (dict, pybamm.BaseModel))
        assert isinstance(tweet.chemistry, str)
        assert isinstance(tweet.is_experiment, bool)
        assert isinstance(tweet.is_comparison, bool)
        assert isinstance(tweet.testing, bool)

        tweet.upload_init()

        assert tweet.processing_info is None

        tweet.upload_append()
        tweet.upload_finalize()
        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")


if __name__ == "__main__":
    unittest.main()
