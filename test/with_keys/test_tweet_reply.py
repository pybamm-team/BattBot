import os
import unittest
from bot.twitter_api.tweet_reply import Reply


class TestTweetReply(unittest.TestCase):
    def test_tweet_reply(self):

        request_examples = (
            "https://github.com/pybamm-team/BattBot/blob/main/REQUEST_EXAMPLES.md"
        )

        reply = Reply(testing=True)
        original_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

        self.assertIsInstance(original_id, int)

        reply.store_tweet_id(original_id, "bot/last_seen_id.txt")
        retrieved_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

        self.assertIsInstance(retrieved_id, int)
        self.assertEqual(retrieved_id, original_id)

        tweet_text = (
            "Compare SPM, SPMe and DFN model with Chen2020 parameters with a 1C"
            " discharge at 278.15K".lower()
        )
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = (
            "Compare SPMe and DFN model with Chen2020 parameters with a 1C discharge at"
            " 278.15K".lower()
        )
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = (
            "Compare SPM and DFN model with Chen2020 parameters with a 1C discharge at"
            " 278.15K".lower()
        )
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = (
            "Compare SPM and DFN model with Marquis2019 parameters with a 1C discharge"
            " at 278.15K".lower()
        )
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = (
            "Compare SPM and DFN model with Ai2020 parameters with a 0.5C discharge at"
            " 278.15K".lower()
        )
        reply.generate_reply(tweet_text)

        assert os.path.exists("plot.gif")
        os.remove("plot.gif")

        tweet_text = (
            "Compare DFN model with Chen2020 parameters with a 1C discharge at 278.15K"
            .lower()
        )
        with self.assertRaisesRegex(
            Exception,
            "Please provide atleast 2 models. Some tweet examples -"
            f" {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = "Chen2020 parameters".lower()
        with self.assertRaisesRegex(
            Exception,
            f"Please provide atleast 1 model. Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = "Compare SPMe and DFN model withChen2020 parameters".lower()
        with self.assertRaisesRegex(
            Exception,
            "Please provide a parameter set in the format - Chen2020 parameters - "
            + f"Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = (
            "SPM and DFN model with Ai2020 parameters with a 0.5C discharge at 278.15K"
            .lower()
        )
        with self.assertRaisesRegex(
            Exception,
            "I'm sorry, I couldn't understand the requested simulation. "
            + f"Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = (
            "Compare spm and spme at a 6C discharge at fgK with Chen2020 parameters"
            .lower()
        )
        with self.assertRaisesRegex(
            Exception,
            "Please provide 'Ambient temperature' in the format - "
            + f"273.15K. Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = (
            "Compare spm and spme at a 6C discharge with Chen2020 parameters".lower()
        )
        with self.assertRaisesRegex(
            Exception,
            "Please provide 'Ambient temperature' in the format - "
            + f"273.15K. Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = "Compare spm and spme at 280K with Chen2020 parameters".lower()
        with self.assertRaisesRegex(
            Exception,
            "Please provide 'C rate' in the format - "
            + f"1C. Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        tweet_text = (
            "Compare spm and spme at 280K at a discharge of fgC with Chen2020"
            " parameters".lower()
        )
        with self.assertRaisesRegex(
            Exception,
            "Please provide 'C rate' in the format - "
            + f"1C. Some tweet examples - {request_examples}",
        ):
            reply.generate_reply(tweet_text)

        reply.reply()


if __name__ == "__main__":
    unittest.main()
