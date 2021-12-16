import argparse
from os import listdir, path
from json import load
from time import sleep

from scrapy.crawler import CrawlerProcess
from articleservice.ArticleService import ArticleService
from service.Service import Service
from twitterservice.TwitterService import TwitterService

service = Service()
path_to_json = path.join(path.dirname(__file__), '..', 'files', 'articles')

def saveTweets():
  tweets = TwitterService().extract_tweets('covid masks')
  service.saveTweets(tweets)

def __crawlArticles():
  process = CrawlerProcess()
  process.crawl(ArticleService)
  process.start()

def __loadArticles(files):
  jsons = []
  for file in files:
     with open(path.join(path_to_json, file)) as json:
        json_text = load(json)
        jsons.append(json_text)
  return jsons

def saveArticles():
  # __crawlArticles()
  files = [pos_json for pos_json in listdir(path_to_json)]
  loaded_files = __loadArticles(files)
  service.saveArticles(loaded_files)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('process', help='type of process that you may execute')
    args = parser.parse_args()
    if args.process == 'savetweets':
       saveTweets()
    if args.process == 'savearticles':
      saveArticles()
