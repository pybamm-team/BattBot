import unittest
import os
import pybamm
from bot.tweet_plot import Tweet


class TestTweetPlot(unittest.TestCase):
    def test_tweet_graph(self):
        tweet = Tweet(
            testing=True, choice="degradation comparison (summary variables)"
        )

        self.assertIsNone(tweet.media_id)
        self.assertIsInstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        self.assertIsNone(tweet.processing_info)
        self.assertIsInstance(tweet.model, pybamm.BaseModel)
        self.assertIsInstance(tweet.chemistry, dict)
        self.assertIsInstance(tweet.is_experiment, bool)
        self.assertTrue(tweet.is_experiment)
        self.assertIsInstance(tweet.cycle, list)
        self.assertIsInstance(tweet.cycle[0], tuple)
        self.assertIsInstance(tweet.number, int)
        self.assertIsInstance(tweet.is_comparison, bool)
        self.assertIsInstance(tweet.testing, bool)

        tweet.upload_init()

        self.assertIsNotNone(tweet.media_id)

        tweet.upload_append()
        tweet.upload_finalize()
        tweet.tweet()

        self.assertIsNotNone(tweet.config)
        f = open("config.txt")
        text = f.read()
        self.assertIsInstance(text, str)
        f.close()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True, choice="non-degradation comparisons")

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

        tweet.upload_init()

        self.assertIsNotNone(tweet.media_id)

        tweet.upload_append()
        tweet.upload_finalize()

        self.assertIsNotNone(tweet.processing_info)

        tweet.tweet()

        self.assertIsNotNone(tweet.config)
        f = open("config.txt")
        text = f.read()
        self.assertIsInstance(text, str)
        f.close()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        tweet = Tweet(testing=True)

        self.assertIsNone(tweet.media_id)
        self.assertIsInstance(tweet.plot, str)
        assert os.path.exists(tweet.plot)
        self.assertIsNone(tweet.processing_info)
        self.assertTrue(
            isinstance(tweet.model, dict)
            or isinstance(tweet.model, pybamm.BaseModel)
        )
        self.assertIsInstance(tweet.chemistry, dict)
        self.assertIsInstance(tweet.is_experiment, bool)
        self.assertIsInstance(tweet.is_comparison, bool)
        self.assertIsInstance(tweet.testing, bool)

        tweet.upload_init()

        self.assertIsNone(tweet.processing_info)

        tweet.upload_append()
        tweet.upload_finalize()
        tweet.tweet()

        self.assertIsNotNone(tweet.config)
        f = open("config.txt")
        text = f.read()
        self.assertIsInstance(text, str)
        f.close()

        assert not os.path.exists("plot.gif")
        assert not os.path.exists("plot.png")

        os.remove("config.txt")


if __name__ == "__main__":
    unittest.main()
