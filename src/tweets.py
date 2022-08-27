from os import path

from service.Service import Service
from twitterservice.TwitterService import TwitterService

service = Service()
path_to_json = path.join(path.dirname(__file__), "..", "files", "articles")


def saveTweets():
    tweets = TwitterService().extract_tweets("covid masks")
    service.saveTweets(tweets)


def cleanTweets():
    service.cleanTweets()
