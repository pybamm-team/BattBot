import os
import sys
import time
import random
import requests
import multiprocessing
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

    def __init__(self, testing=False, choice=None):
        """
        Defines video tweet properties
        """
        while True:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            # 0: pre-defined model with a pre-defined chemistry
            # 1: experiment with summary variable
            # 2: experiment without summary variables
            # 3: comparison plots
            if choice is None:
                choice = random.randint(0, 3)

            p = multiprocessing.Process(target=random_plot_generator, args=(
                return_dict,
                {
                    "testing": testing,
                    "choice": choice,
                    "chemistry": None,
                    "provided_degradation": True
                }
            )
            )

            p.start()
            if choice == 0:
                p.join(300)
            elif choice == 1:
                p.join(1200)
            elif choice == 2:
                p.join(450)
            elif choice == 3:
                p.join(1200)

            if p.is_alive():    # pragma: no cover
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                p.kill()
                p.join()
            else:   # pragma: no cover
                break

        if os.path.exists("plot.gif"):
            self.plot = "plot.gif"
        else:
            self.plot = "plot.png"
        self.total_bytes = os.path.getsize(self.plot)
        self.media_id = None
        self.processing_info = None
        self.model = return_dict["model"]
        self.parameter_values = return_dict["parameter_values"]
        self.time = return_dict["time_array"]
        self.chemistry = return_dict["chemistry"]
        self.solver = return_dict["solver"]
        self.is_experiment = return_dict["is_experiment"]
        self.cycle = return_dict["cycle"]
        self.number = return_dict["number"]
        self.is_comparison = return_dict["is_comparison"]
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

        req = self.post_request(media_endpoint_url, request_data, oauth)

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

            self.post_request(media_endpoint_url, request_data, oauth, files)

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

        req = self.post_request(media_endpoint_url, request_data, oauth)

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

    def post_request(self, url, data, auth, files=None):
        """
        Posts a request on the Twitter API and makes
        sure that the given post request succeeds
        """
        while True:
            if files is None:
                req = requests.post(
                    url=url,
                    data=data,
                    auth=auth
                )
            else:
                req = requests.post(
                    url=url,
                    data=data,
                    files=files,
                    auth=auth
                )
            if (
                req.status_code >= 200 and req.status_code <= 299
            ):
                break
            else:  # pragma: no cover
                print(req.status_code)
                print(req.text)
                print(
                    "Twitter API internal error."
                    + " Trying again in 5 minutes"
                )
                time.sleep(300)

        return req

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
            self.post_request(post_tweet_url, request_data, oauth)
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
