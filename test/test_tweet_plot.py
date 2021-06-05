import unittest
import os
import pybamm
from bot.tweet_plot import Tweet


class TestTweetPlot(unittest.TestCase):
    def test_tweet_graph(self):
        tweet = Tweet(testing=True)

        self.assertIsNone(tweet.media_id)
        self.assertIsInstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        self.assertIsNone(tweet.processing_info)
        self.assertIsInstance(tweet.model, pybamm.BaseModel)
        self.assertIsInstance(tweet.parameter_values, pybamm.ParameterValues)
        self.assertIsInstance(tweet.time, list)
        self.assertIsInstance(tweet.chemistry, dict)
        self.assertIsInstance(tweet.solver, pybamm.BaseSolver)
        self.assertIsInstance(tweet.is_experiment, bool)
        self.assertIsNone(tweet.cycle)
        self.assertIsNone(tweet.number)
        self.assertIsInstance(tweet.is_comparison, bool)
        self.assertIsInstance(tweet.testing, bool)

        tweet.upload_init()

        self.assertIsNotNone(tweet.media_id)

        tweet.upload_append()
        tweet.upload_finalize()

        self.assertIsNotNone(tweet.processing_info)

        tweet.tweet()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")


if __name__ == "__main__":
    unittest.main()
