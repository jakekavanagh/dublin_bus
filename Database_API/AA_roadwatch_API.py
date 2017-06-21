from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key = "IN2I9yFJ1tehBl9321VJYWO8d"
consumer_secret = "QR0T5hpBPn3CvaXIwzE7S9fIwAsfVlPtWOhth22VqBfaN0e9sH"
access_token = "876794679702032385-qBLuTCnaqiXBWcqLkohhPgbfNGQF9bx"
access_secret = "jUkcx29kXg4R3r7VLVuBhtmTwj0mEvK59k594rtACAoop"


class listener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Dublin"])

