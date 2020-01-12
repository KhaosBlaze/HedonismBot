from twitter import *
from secrets import *

t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

def post_status(tweet):
	t.statuses.update(status=tweet, tweet_mode="extended")
