import tweepy
from requests_oauthlib import OAuth1

from twitter_api.api_keys import Keys
from twitter_api.tweet_reply import Reply

# setting up the API keys, tweepy auth and tweepy api object
keys = Keys()
oauth = OAuth1(
    keys.CONSUMER_KEY,
    client_secret=keys.CONSUMER_SECRET,
    resource_owner_key=keys.ACCESS_TOKEN,
    resource_owner_secret=keys.ACCESS_TOKEN_SECRET,
)
auth = tweepy.OAuth1UserHandler(
    keys.CONSUMER_KEY,
    keys.CONSUMER_SECRET,
    keys.ACCESS_TOKEN,
    keys.ACCESS_TOKEN_SECRET,
)
api = tweepy.API(auth)


def sync_last_seen_id(testing=False):
    """
    Syncs the ID of the last seen tweet (by the bot) on GitHub
    with the Heroku deployment.

    Parameters
    ----------
        testing : bool
    """
    tweet_reply = Reply()

    if testing:
        last_seen_id = tweet_reply.retrieve_tweet_id("bot/last_seen_id.txt")
    else:  # pragma: no cover
        last_seen_id = tweet_reply.retrieve_tweet_id("last_seen_id.txt")

    # retrieving all the mentions after the tweet with id=last_seen_id
    mentions = api.mentions_timeline(since_id=last_seen_id, tweet_mode="extended")

    # iterating through all the mentions if not testing
    if not testing:
        for mention in reversed(mentions):
            if "#battbot" in mention.full_text.lower():
                # scraping all the replies of the tweet with id=last_seen_id
                replies = tweepy.Cursor(
                    api.search_tweets,
                    q=f"to:{mention.user.screen_name}",
                    since_id=mention._json["id"],
                    tweet_mode="extended",
                ).items()

                # iterating through the replies
                for reply in replies:
                    # if the bot has replied
                    if (
                        reply._json["in_reply_to_status_id"] == mention._json["id"]
                        and reply._json["user"]["screen_name"] == "battbot_"
                    ):
                        # storing the id
                        tweet_reply.store_tweet_id(
                            mention._json["id"], "last_seen_id.txt"
                        )
                        print(
                            mention.user.screen_name
                            + " "
                            + mention.full_text
                            + " "
                            + str(mention._json["id"])
                        )


if __name__ == "__main__":
    sync_last_seen_id()
