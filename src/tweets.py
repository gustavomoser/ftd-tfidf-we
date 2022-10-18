from service.Service import Service
from twitter.TwitterScraper import TwitterScraper

service = Service()


def saveTweets():
    tweets = TwitterScraper().extract_tweets("covid masks")
    service.saveTweets(tweets)


def cleanTweets():
    service.cleanTweets()
