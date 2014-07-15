#!/usr/bin/python -i
"""This script allows for walking a Twitter users' timeline backwards, 50 tweets
at a time. Note the -i in the shebang line. It's intended to be used through the
REPL. The first 50 tweets are printed out. The next can be fetched and printed
via
    pprint.pprint(user_timeline.next())

For this to work, create an api.cfg file in the same directory as this script.
Populate it as follows:

    [twitter]
    consumer_key = ...
    consumer_secret = ...
    access_token_key = ...
    access_token_secret = ...

Replace the '...'s with the appropriate values from your own API keys, obtained
at https://apps.twitter.com/


Example usage:
    ./twitter_stream_crawler.py @preston4tw
"""

# stdlib
import ConfigParser
import pprint
import sys

# 3rdparty
import twitter # pip install python-twitter

config = ConfigParser.ConfigParser()
config.read("api.cfg")
api = twitter.Api(consumer_key=config.get("twitter", "consumer_key"),
                  consumer_secret=config.get("twitter", "consumer_secret"),
                  access_token_key=config.get("twitter", "access_token_key"),
                  access_token_secret=config.get("twitter", "access_token_secret")
                 )

def all_tweets(username):
    """Create a generator that grabs a users' 50 most recent tweets and then
    walks backwards through them, 50 at a time"""
    tweet_count = 50
    tweets = api.GetUserTimeline(screen_name=username, count=tweet_count)
    next_tweets = api.GetUserTimeline(screen_name=username, count=tweet_count, max_id=tweets[-1].id-1)
    while tweets[0].id != next_tweets[0].id:
        yield [tweet.text for tweet in tweets]
        tweets = next_tweets
        next_tweets = api.GetUserTimeline(screen_name=username, count=tweet_count, max_id=tweets[-1].id-1)


# Main
twitter_username = sys.argv[1]
user_timeline = all_tweets(twitter_username)
pprint.pprint(user_timeline.next())


# vim: ts=4 sts=4 sw=4 expandtab
