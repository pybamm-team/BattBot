import unittest
import os
import pybamm   # noqa
from bot.twitter_api.tweet_plot import Tweet


class TestTweet(unittest.TestCase):
    def test_tweet(self):
        # tweet = Tweet(
        #     testing=True, choice="degradation comparison"
        # )

        # self.assertIsNone(tweet.media_id)
        # self.assertIsInstance(tweet.plot, str)
        # assert os.path.exists(tweet.plot)
        # self.assertIsNone(tweet.processing_info)
        # self.assertIsInstance(tweet.model, pybamm.BaseModel)
        # self.assertIsInstance(tweet.chemistry, dict)
        # self.assertIsInstance(tweet.is_experiment, bool)
        # self.assertTrue(tweet.is_experiment)
        # self.assertIsInstance(tweet.cycle, list)
        # self.assertIsInstance(tweet.cycle[0], tuple)
        # self.assertIsInstance(tweet.number, int)
        # self.assertIsInstance(tweet.is_comparison, bool)
        # self.assertFalse(tweet.is_comparison)
        # self.assertIsInstance(tweet.testing, bool)
        # self.assertIsInstance(tweet.param_to_vary, str)
        # self.assertIsInstance(tweet.varied_values, list)
        # self.assertIsNone(tweet.params)
        # self.assertIsInstance(tweet.degradation_mode, str)
        # self.assertIsInstance(tweet.degradation_value, str)

        # tweet.upload_init()

        # self.assertIsNotNone(tweet.media_id)

        # tweet.upload_append()
        # tweet.upload_finalize()
        # tweet.tweet()

        # assert not os.path.exists("plot.gif")
        # assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True, choice="model comparison")

        self.assertIsNone(tweet.media_id)
        self.assertIsInstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        self.assertIsNone(tweet.processing_info)
        self.assertIsInstance(tweet.model, dict)
        self.assertIsInstance(tweet.chemistry, dict)
        self.assertIsInstance(tweet.is_experiment, bool)
        self.assertIsInstance(tweet.is_comparison, bool)
        self.assertTrue(tweet.is_comparison)
        self.assertIsInstance(tweet.testing, bool)
        self.assertIsInstance(tweet.varied_values, dict)
        self.assertIsInstance(tweet.params, dict)
        self.assertIsNone(tweet.degradation_mode, None)
        self.assertIsNone(tweet.degradation_value, None)

        tweet.upload_init()

        self.assertIsNotNone(tweet.media_id)

        tweet.upload_append()
        tweet.upload_finalize()

        self.assertIsNotNone(tweet.processing_info)

        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        # tweet = Tweet(testing=True, choice="parameter comparison")

        # self.assertIsNone(tweet.media_id)
        # self.assertIsInstance(tweet.plot, str)
        # assert os.path.exists(tweet.plot)
        # self.assertIsNone(tweet.processing_info)
        # self.assertIsInstance(tweet.model, dict)
        # self.assertIsInstance(tweet.chemistry, dict)
        # self.assertIsInstance(tweet.is_experiment, bool)
        # self.assertIsInstance(tweet.is_comparison, bool)
        # self.assertTrue(tweet.is_comparison)
        # self.assertIsInstance(tweet.testing, bool)
        # self.assertIsInstance(tweet.varied_values, list)
        # self.assertIsInstance(tweet.params, dict)
        # self.assertIsNone(tweet.degradation_mode, None)
        # self.assertIsNone(tweet.degradation_value, None)

        # tweet.upload_init()

        # self.assertIsNotNone(tweet.media_id)

        # tweet.upload_append()
        # tweet.upload_finalize()

        # self.assertIsNotNone(tweet.processing_info)

        # tweet.tweet()

        # assert not os.path.exists("plot.gif")
        # assert not os.path.exists("plot.png")

        # tweet = Tweet(testing=True)

        # self.assertIsNone(tweet.media_id)
        # self.assertIsInstance(tweet.plot, str)
        # assert os.path.exists(tweet.plot)
        # self.assertIsNone(tweet.processing_info)
        # self.assertTrue(
        #     isinstance(tweet.model, dict)
        #     or isinstance(tweet.model, pybamm.BaseModel)
        # )
        # self.assertIsInstance(tweet.chemistry, dict)
        # self.assertIsInstance(tweet.is_experiment, bool)
        # self.assertIsInstance(tweet.is_comparison, bool)
        # self.assertIsInstance(tweet.testing, bool)

        # tweet.upload_init()

        # self.assertIsNone(tweet.processing_info)

        # tweet.upload_append()
        # tweet.upload_finalize()
        # tweet.tweet()

        # assert not os.path.exists("plot.gif")
        # assert not os.path.exists("plot.png")


if __name__ == "__main__":
    unittest.main()
