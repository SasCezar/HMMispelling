import tweepy
import logging


class TwitterService(object):

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self._consumer_key_ = consumer_key
        self._consumer_secret_ = consumer_secret
        self._access_key_ = access_key
        self._access_secret_ = access_secret

        self._api_ = None

    @property
    def api(self):
        return self._api_

    def connect(self):
        auth = tweepy.OAuthHandler(self._consumer_key_, self._consumer_secret_)
        auth.secure = True
        auth.set_access_token(self._access_key_, self._access_secret_)
        api = tweepy.API(auth)
        self._api_ = api

        return self


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self._subscribers_ = []

    @property
    def subscribers(self):
        return self._subscribers_

    @subscribers.setter
    def subscribers(self, value):
        self._subscribers_ = value

    def on_status(self, status):
        logging.info(status.text)
        for sub in self.subscribers:
            sub(status)

    def on_error(self, status_code):
        logging.debug(status_code)
        pass

    def on_disconnect(self, notice):
        logging.debug(notice)
        pass

def test():
    consumer_key = "AHB6bSwBcXsnLzFMh4wDbne27"
    consumer_secret = "YCYo9Jv9d3QSbvIZDKYyw1rFccDVLbyjJl7PCZW1ipe304Evlw"
    access_token = "3531429916-GJBeBqGlMSREIpOhPuH2LZzavgzkVKVP2NiWLGD"
    access_secret = "SlmBNSy1dHcdUw0sthd4oxjpNGLmEtBqnb8Ac48UwszWC"

    twitter_connection = TwitterService(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                        access_key=access_token, access_secret=access_secret)
    twitter_connection.connect()

    api = twitter_connection.api

    stream_listener = TwitterStreamListener()

    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    stream.filter(track=["apple"], languages=["en"], async=True)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    test()
