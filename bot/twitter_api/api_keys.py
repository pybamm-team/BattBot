import os


class Keys:
    def __init__(self):
        self.CONSUMER_KEY = os.environ["CONSUMER_KEY"]
        self.CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
        self.ACCESS_TOKEN = os.environ["ACCESS_KEY"]
        self.ACCESS_TOKEN_SECRET = os.environ["ACCESS_SECRET"]
