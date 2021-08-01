import os
import unittest
from bot.twitter_api.tweet_reply import Reply


class TestTweetReply(unittest.TestCase):
    def test_tweet_reply(self):

        reply = Reply(testing=True)
        original_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

        self.assertIsInstance(original_id, int)

        reply.store_tweet_id(original_id, "bot/last_seen_id.txt")
        retrieved_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

        self.assertIsInstance(retrieved_id, int)
        self.assertEqual(retrieved_id, original_id)

        tweet_text = "Compare SPM, SPMe and DFN model with Chen2020 parameters".lower()
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = "Compare SPMe and DFN model with Chen2020 parameters".lower()
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = "Compare SPM and DFN model with Chen2020 parameters".lower()
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = "Compare DFN model with Chen2020 parameters".lower()
        with self.assertRaises(Exception) as e:
            reply.generate_reply(tweet_text)
            self.assertEqual(
                str(e.exception),
                "Please provide atleast 2 models. Some tweet examples - ",
            )

            tweet_text = "Compare DFN model with Chen2020 parameters".lower()
            reply.generate_reply(tweet_text)
            self.assertEqual(
                str(e.exception),
                "Please provide atleast 2 models. Some tweet examples - ",
            )

            tweet_text = "Chen2020 parameters".lower()
            reply.generate_reply(tweet_text)
            self.assertEqual(
                str(e.exception),
                "Please provide atleast 1 model. Some tweet examples - ",
            )

            tweet_text = "Compare SPMe and DFN model withChen2020 parameters".lower()
            reply.generate_reply(tweet_text)
            self.assertEqual(
                str(e.exception),
                "Please provide a parameter set in the format - Chen2020 parameters - "
                + "Some tweet examples - ",
            )

            tweet_text = "SPM and DFN model with Chen2020 parameters".lower()
            reply.generate_reply(tweet_text)
            self.assertEqual(
                str(e.exception),
                "I'm sorry, I couldn't understand the requested simulation. "
                + "Some tweet examples - ",
            )


if __name__ == "__main__":
    unittest.main()
