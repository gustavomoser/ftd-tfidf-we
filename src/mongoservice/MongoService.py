from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from os import path, environ

class MongoService: 
  def __getDatabase(self):
    load_dotenv(dotenv_path=path.join(path.dirname(__file__), '..', '..', '.env'))
    uri = environ.get('MONGO_URI')
    client = MongoClient(uri)
    return client['tweets_articles']

  def __getTweetCollection(self):
    conn = self.__getDatabase()
    return conn['tweets']

  def __getArticleCollection(self):
    conn = self.__getDatabase()
    return conn['articles']

  def getTweets(self):
    tweets = self.__getTweetCollection()
    return tweets.find()

  def filterTweetsById(self, tweets):
    tweetColl = self.__getTweetCollection()
    ids = [tweet['id'] for tweet in tweets]
    exists = tweetColl.find({ "id": { "$in": ids}})

  def getTweets(self):
    tweets = self.__getTweetCollection()
    return tweets.find()

  def filterTweetsById(self, tweets):
    ids = [tweet['id'] for tweet in tweets]
    tweetColl = self.__getTweetCollection()
    exists = [tweet['id'] for tweet in tweetColl.find({ "id": { "$in": ids}})]
    return list(filter(lambda t: t['id'] not in exists, tweets))

  def saveTweets(self, tweets):
    filtered = self.filterTweetsById(tweets)
    if filtered:
      tweetColl = self.__getTweetCollection()
      tweetColl.insert_many(filtered)

  def getArticles(self):
    articles = self.__getArticleCollection()
    return articles.find()

  def filterArticlesByTitle(self, articles):
    titles = [article['title'] for article in articles]
    articleColl = self.__getArticleCollection()
    exists = [article['title'] for article in articleColl.find({ 'title': { '$in': titles }})]
    return list(filter(lambda t: t['title'] not in exists, articles))
  
  def saveArticles(self, articles):
    articleColl = self.__getArticleCollection()
    filtered = self.filterArticlesByTitle(articles)
    if filtered:
      articleColl.insert_many(filtered)
