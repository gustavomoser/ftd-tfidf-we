import tweepy
from dotenv import load_dotenv
from os import path, environ

class TwitterService:
  def extract_tweets(self, query):
    load_dotenv(dotenv_path=path.join(path.dirname(__file__), '..', '..'))
    
    bearer = environ.get('BEARER_TOKEN')
    
    client = tweepy.Client(bearer_token=bearer)
    
    query = f'{query} -is:retweet'
    
    result = client.search_all_tweets(query=query, tweet_fields=[])
    
    for tweet in result:
      self.persist(tweet)


  def persist(self, tweet):
    # TODO implement mongo interaction
    print(tweet)