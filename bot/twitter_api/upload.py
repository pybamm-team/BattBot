import logging
import os
import sys
import time

import requests
import tweepy
from requests_oauthlib import OAuth1

from twitter_api.api_keys import Keys


# Official Twitter API example by Twitter Developer Relations:
# https://github.com/twitterdev/large-video-upload-python
class Upload:
    """
    Uploads a media to the twitter API by dividing it into chunks.

    Parameters
    ----------
        plot : str
            Relative path of the file that has to be uploaded. Should be used
            during testing. In a subclasses, it can be accessed as `self.plot`,
            thus passing it as a parameter will be redundant.
        total_bytes : numerical
            Size of the passed file. Should be used during testing. In a subclasses,
            it can be accessed as `self.total_bytes`, thus passing it as a parameter
            will be redundant.
    """

    def __init__(self, plot=None, total_bytes=None):
        self.media_endpoint_url = "https://upload.twitter.com/1.1/media/upload.json"
        self.post_tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        self.keys = Keys()
        self.oauth = OAuth1(
            self.keys.CONSUMER_KEY,
            client_secret=self.keys.CONSUMER_SECRET,
            resource_owner_key=self.keys.ACCESS_TOKEN,
            resource_owner_secret=self.keys.ACCESS_TOKEN_SECRET,
        )
        self.auth = tweepy.OAuth1UserHandler(
            self.keys.CONSUMER_KEY,
            self.keys.CONSUMER_SECRET,
            self.keys.ACCESS_TOKEN,
            self.keys.ACCESS_TOKEN_SECRET,
        )
        self.api = tweepy.API(self.auth)
        self.total_bytes = total_bytes
        self.media_id = None
        self.processing_info = None
        self.plot = plot

    def upload_init(self):
        """
        Initializes Upload
        """
        print("INIT")

        # initiate uploading the data
        if os.path.exists("plot.gif"):
            request_data = {
                "command": "INIT",
                "media_type": "image/gif",
                "total_bytes": self.total_bytes,
                "media_category": "tweet_gif",
            }
        else:
            request_data = {
                "command": "INIT",
                "media_type": "image/png",
                "total_bytes": self.total_bytes,
                "media_category": "tweet_image",
            }

        # post the initial request
        req = self.post_request(self.media_endpoint_url, request_data, self.oauth)

        # extract media id for the GIF
        media_id = req.json()["media_id"]

        self.media_id = media_id

        print("Media ID: %s" % str(media_id))

    def upload_append(self):
        """
        Uploads media in chunks and appends to chunks uploaded
        """
        segment_id = 0
        bytes_sent = 0
        with open(self.plot, "rb") as file:
            # upload the media in chunks
            while bytes_sent < self.total_bytes:
                # initialise a single chunk
                chunk = file.read(4 * 1024 * 1024)

                print("APPEND")

                # append the chunks
                request_data = {
                    "command": "APPEND",
                    "media_id": self.media_id,
                    "segment_index": segment_id,
                }

                files = {"media": chunk}

                # post request to append the chunks
                self.post_request(
                    self.media_endpoint_url, request_data, self.oauth, files
                )

                segment_id = segment_id + 1
                bytes_sent = file.tell()

                print(f"{bytes_sent!s} of {self.total_bytes!s} bytes uploaded")

            print("Upload chunks complete.")

    def upload_finalize(self):
        """
        Finalizes uploads and starts video processing
        """
        print("FINALIZE")

        # finalize the media upload
        request_data = {"command": "FINALIZE", "media_id": self.media_id}

        # send a request for finalizing the media upload
        req = self.post_request(self.media_endpoint_url, request_data, self.oauth)

        print(req.json())

        # extract the processing information of the GIF and check status
        # until it either passes or fails
        self.processing_info = req.json().get("processing_info", None)
        self.check_status()

    def check_status(self):
        """
        Checks video processing status
        """
        if self.processing_info is None:  # pragma: no cover
            return

        state = self.processing_info["state"]

        print("Media processing status is %s " % state)

        if state == "succeeded":
            return

        if state == "failed":  # pragma: no cover
            sys.exit(0)

        check_after_secs = self.processing_info["check_after_secs"]

        print("Checking after %s seconds" % str(check_after_secs))
        time.sleep(check_after_secs)

        print("STATUS")

        request_params = {"command": "STATUS", "media_id": self.media_id}

        req = requests.get(
            url=self.media_endpoint_url, params=request_params, auth=self.oauth
        )

        self.processing_info = req.json().get("processing_info", None)
        self.check_status()

    def post_request(self, url, data, auth, files=None):
        """
        Posts a request on the Twitter API and makes
        sure that the given post request succeeds.

        Parameters
        ---------
            url : str
                Twitter API endpoint.
            data : dict
                The request data.
            auth : request_oauthlib.OAuth1
                Twitter developer account credentials.
            files : file
                default : None
                Single chunk of a media file.
        """
        # logging configs
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # try to post request, if the API gives an error, sleep for 5 minutes
        # and then try again
        while True:
            if files is None:
                req = requests.post(url=url, data=data, auth=auth)
            else:
                req = requests.post(url=url, data=data, files=files, auth=auth)
            if req.status_code >= 200 and req.status_code <= 299:
                break
            else:  # pragma: no cover
                logger.info(req.status_code)
                logger.info(req.text)
                logger.info(
                    "Twitter API internal error." + " Trying again in 5 minutes"
                )
                time.sleep(300)

        return req
