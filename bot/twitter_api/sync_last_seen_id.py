import tweepy
from twitter_api.api_keys import Keys
from twitter_api.tweet_reply import Reply


# setting up the API keys, tweepy auth and tweepy api object
keys = Keys()
api = keys.api


def sync_last_seen_id(testing=False):
    """
    Syncs the ID of the last seen tweet (by the bot) on GitHub
    with the Heroku deployment.
    Parameters:
        testing: bool
    """
    tweet_reply = Reply()

    if testing:
        last_seen_id = tweet_reply.retrieve_tweet_id(
            "bot/last_seen_id.txt"
        )
    else:   # pragma: no cover
        last_seen_id = tweet_reply.retrieve_tweet_id("last_seen_id.txt")

    # retreiving all the mentions after the tweet with id=last_seen_id
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

    # iterating through all the mentions if not testing
    if not testing:  # pragma: no cover
        for mention in reversed(mentions):
            if '#battbot' in mention.full_text.lower():

                # scraping all the replies of the tweet with id=last_seen_id
                replies = tweepy.Cursor(
                    api.search,
                    q='to:{}'.format(mention.user.screen_name),
                    since_id=mention._json["id"],
                    tweet_mode='extended'
                ).items()

                # iterating through the replies
                for reply in replies:

                    # if the bot has replied
                    if(
                        reply._json['in_reply_to_status_id'] == mention._json["id"]    # noqa
                        and mention.user.screen_name == "Saransh_test"
                    ):
                        # storing the id
                        tweet_reply.store_tweet_id(
                            mention._json["id"], "last_seen_id.txt"
                        )
                        print(
                            mention.user.screen_name + " "
                            + mention.full_text + " "
                            + str(mention._json["id"])
                        )


if __name__ == "__main__":
    sync_last_seen_id()
