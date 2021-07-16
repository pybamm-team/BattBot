import unittest
from bot.tweet_reply import Reply


class TestTweetReply(unittest.TestCase):
    def test_tweet_reply(self):

        reply = Reply(testing=True)
        id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

        self.assertIsInstance(id, int)

        reply.store_tweet_id(id, "bot/last_seen_id.txt")
        reply.reply_to_tweet()
