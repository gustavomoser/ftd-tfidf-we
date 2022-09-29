from os import environ, path

import tweepy
from dotenv import load_dotenv


class TwitterService:
    def extract_tweets(self, query):
        load_dotenv(dotenv_path=path.join(path.dirname(__file__), "..", "..", ".env"))

        bearer = environ.get("BEARER_TOKEN")

        client = tweepy.Client(bearer_token=bearer, wait_on_rate_limit=True)

        query = f"{query} -is:retweet"

        result = client.search_recent_tweets(query=query, max_results=100)

        tweets = [{"id": tweet.id, "text": tweet.text} for tweet in result.data]

        return tweets
