from os import listdir, path
from json import load

from scrapy.crawler import CrawlerProcess
from articleservice.ArticleService import ArticleService
from service.Service import Service

service = Service()
path_to_json = path.join(path.dirname(__file__), "..", "assets", "articles")


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
    __crawlArticles()
    files = [pos_json for pos_json in listdir(path_to_json)]
    loaded_files = __loadArticles(files)
    service.saveArticles(loaded_files)
