import unittest

from bot.twitter_api.sync_last_seen_id import sync_last_seen_id


class TestSyncLastSeenId(unittest.TestCase):
    def test_sync_last_seen_id(self):
        sync_last_seen_id(testing=True)


if __name__ == "__main__":
    unittest.main()
