import tweepy
from dotenv import load_dotenv
from os import path, environ

class TwitterService:
  def extract_tweets(self, query):
    load_dotenv(dotenv_path=path.join(path.dirname(__file__), '..', '..', '.env'))
    
    bearer = environ.get('BEARER_TOKEN')
    
    client = tweepy.Client(bearer_token=bearer, wait_on_rate_limit=True)
    
    query = f'{query} -is:retweet'
    
    result = client.search_recent_tweets(query=query, max_results=100) # max_results=100 tweet_fields=[]
    
    for tweet in result:
      self.persist(tweet)


  def persist(self, tweet):
    # TODO implement mongo interaction
    print(tweet)

# service = TwitterService()
# service.extract_tweets(query="covid masks")