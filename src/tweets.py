from os import path

from service.Service import Service
from twitterservice.TwitterScraper import TwitterScraper

service = Service()
path_to_json = path.join(path.dirname(__file__), "..", "files", "articles")


def saveTweets():
    tweets = TwitterScraper().extract_tweets("covid masks")
    service.saveTweets(tweets)


def cleanTweets():
    service.cleanTweets()
