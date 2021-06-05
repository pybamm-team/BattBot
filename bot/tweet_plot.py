import os
import sys
import time
import requests
import matplotlib.pyplot as plt
from requests_oauthlib import OAuth1
from plotting.random_plot_generator import random_plot_generator
from information.information import information


media_endpoint_url = 'https://upload.twitter.com/1.1/media/upload.json'
post_tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_KEY"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_SECRET"]

oauth = OAuth1(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET
)


# Official Twitter API example by Twitter Developer Relations:
# https://github.com/twitterdev/large-video-upload-python
class Tweet(object):

    def __init__(self, testing=False, provided_choice=None):
        """
        Defines video tweet properties
        """
        (
            model,
            parameter_values,
            time,
            chemistry,
            solver,
            is_experiment,
            cycle,
            number,
            is_comparison,
        ) = random_plot_generator(
            testing=testing,
            provided_choice=provided_choice
        )
        if os.path.exists("plot.gif"):
            self.plot = "plot.gif"
        else:
            self.plot = "plot.png"
        self.total_bytes = os.path.getsize(self.plot)
        self.media_id = None
        self.processing_info = None
        self.model = model
        self.parameter_values = parameter_values
        self.time = time
        self.chemistry = chemistry
        self.solver = solver
        self.is_experiment = is_experiment
        self.cycle = cycle
        self.number = number
        self.is_comparison = is_comparison
        self.testing = testing

    def upload_init(self):
        """
        Initializes Upload
        """
        print('INIT')

        if os.path.exists("plot.gif"):
            request_data = {
                'command': 'INIT',
                'media_type': 'image/gif',
                'total_bytes': self.total_bytes,
                'media_category': 'tweet_gif'
            }
        else:
            request_data = {
                'command': 'INIT',
                'media_type': 'image/png',
                'total_bytes': self.total_bytes,
                'media_category': 'tweet_image'
            }

        req = requests.post(
            url=media_endpoint_url, data=request_data, auth=oauth
        )
        print(req.json())
        media_id = req.json()['media_id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))

    def upload_append(self):
        """
        Uploads media in chunks and appends to chunks uploaded
        """
        segment_id = 0
        bytes_sent = 0
        file = open(self.plot, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)

            print('APPEND')

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media': chunk
            }

            req = requests.post(
                url=media_endpoint_url,
                data=request_data,
                files=files,
                auth=oauth
            )

            if req.status_code < 200 or req.status_code > 299:  # pragma: no cover
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print(
                '%s of %s bytes uploaded' % (
                    str(bytes_sent),
                    str(self.total_bytes)
                )
            )

        print('Upload chunks complete.')
        file.close()

    def upload_finalize(self):
        """
        Finalizes uploads and starts video processing
        """
        print('FINALIZE')

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(
            url=media_endpoint_url, data=request_data, auth=oauth
        )
        print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        """
        Checks video processing status
        """
        if self.processing_info is None:    # pragma: no cover
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':  # pragma: no cover
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(
            url=media_endpoint_url, params=request_params, auth=oauth
        )

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def tweet(self):
        """
        Publishes Tweet with attached plot
        """
        tweet_status = (
            information(
                self.chemistry,
                self.model,
                self.solver,
                self.is_experiment,
                self.cycle,
                self.number,
                self.is_comparison
            )
            + ", at time = "
            + str(self.time)
            + " s"

        )

        request_data = {
            'status': tweet_status,
            'media_ids': self.media_id
        }

        if not self.testing:    # pragma: no cover
            req = requests.post(
                url=post_tweet_url, data=request_data, auth=oauth
            )
            print(req.json())
        if os.path.exists("plot.gif"):
            os.remove("plot.gif")
        else:
            os.remove("plot.png")
        plt.close()


if __name__ == '__main__':  # pragma: no cover
    tweet = Tweet()
    tweet.upload_init()
    tweet.upload_append()
    tweet.upload_finalize()
    tweet.tweet()
