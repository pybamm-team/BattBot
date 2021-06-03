import unittest
import os
from bot.tweet_plot import tweet_graph


class TestTweetPlot(unittest.TestCase):
    def tearDown(self):
        assert not os.path.exists("plot.gif")

    def test_tweet_graph(self):
        tweet_graph(testing=True)


if __name__ == "__main__":
    unittest.main()
