import re
from json import dumps
from os import makedirs, path

import nltk
from db.PostgresManager import PostgresManager
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from util import clean

#  NLTK built-in support for dozens of corpora and trained models
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)


class Service:
    ps = PorterStemmer()

    def saveTweets(self, tweets):
        pm = PostgresManager()
        insert = ",".join(
            pm.cursor().mogrify("(%s,%s)", (tweet["id"], tweet["text"])).decode("utf-8")
            for tweet in tweets
        )
        pm.insert(
            "INSERT INTO tweet (id, tweet) VALUES "
            + insert
            + " ON CONFLICT DO NOTHING;"
        )

    def cleanTweets(self):
        pm = PostgresManager()
        base_tweets = pm.fetchAll("SELECT * FROM tweet")
        tweets = [{"id": tt[0], "tweet": clean(tt[1])} for tt in base_tweets]
        insert = ",".join(
            pm.cursor()
            .mogrify("(%s,%s)", (tweet["id"], tweet["tweet"]))
            .decode("utf-8")
            for tweet in tweets
        )
        pm.insert(
            "INSERT INTO tweet_clean (id, tweet) VALUES "
            + insert
            + " ON CONFLICT DO NOTHING;"
        )
        pm.delete("tweet_clean", "tweet IS NULL OR tweet = ''")

    def saveArticles(self, articles):
        pm = PostgresManager()
        for article in articles:
            title = article["title"]
            exists = pm.findOne(
                "SELECT 1 FROM article WHERE title = '{}';".format(title)
            )
            if exists is None:
                id = pm.insertAndReturnId(
                    "INSERT INTO article (title) VALUES (%s) RETURNING id;", (title,)
                )

                authors_list = article["authors"]
                authors = ",".join(
                    pm.cursor().mogrify("(%s,%s)", (id, author)).decode("utf-8")
                    for author in authors_list
                )
                pm.insert(
                    "INSERT INTO author (article_id, name) VALUES " + authors + ";"
                )

                section_list = article["sections"]
                sections = ",".join(
                    pm.cursor()
                    .mogrify(
                        "(%s,%s,%s)",
                        (id, section["section"], section["content"].replace("'", "''")),
                    )
                    .decode("utf-8")
                    for section in section_list
                )
                pm.insert(
                    "INSERT INTO article_section (id, title, content) VALUES "
                    + sections
                    + ";"
                )

    def getArticleSections(self):
        pm = PostgresManager()
        rs = pm.fetchAll("SELECT id, content FROM article_section")

        res = {}
        for result in rs:
            id = result[0]
            content = result[1]
            if id not in res:
                res[id] = content
            else:
                res.update({id: res[id] + " " + content})

        return res

    def getTweets(self):
        pm = PostgresManager()
        rs = pm.fetchAll("SELECT * FROM tweet_clean")

        res = {}
        for result in rs:
            id = result[0]
            content = result[1]
            res.update({id: content})

        return res

    def __textToStemTokens(self, text: str) -> list[str]:
        tokens = nltk.word_tokenize(text)
        stem = []
        for word in tokens:
            if (
                re.fullmatch(r"[a-z]+", word)
                and word not in stopwords.words("english")
                and len(word) > 1
            ):
                stem.append(self.ps.stem(word))
        return stem

    def export(self):
        self.exportFullArticleContentToJson()
        self.exportCleanWordsToJson()
        self.exportFullTweetsToJson()
        self.exportCleanTweetsToJson()

    def exportFullTweetsToJson(self):
        self.writeJsonFile(self.getTweets(), "tweet_full.json")

    def exportCleanTweetsToJson(self):
        export = {}

        tweets = self.getTweets()
        for id, tweet in tweets.items():
            root = self.__textToStemTokens(tweet)
            export.update({id: root})

        self.writeJsonFile(export, "tweet_root_words.json")

    def exportFullArticleContentToJson(self):
        self.writeJsonFile(self.getArticleSections(), "article_full_section.json")

    def exportCleanWordsToJson(self):
        export = {}

        sections = self.getArticleSections()
        for id, section in sections.items():
            tokens = self.__textToStemTokens(section)
            export.update({id: tokens})

        self.writeJsonFile(export, "article_root_words.json")

    def writeJsonFile(self, obj: object, filename: str):
        if not obj or not filename:
            return

        json = dumps(obj)

        directory = path.join(path.dirname(__file__), "..", "..", "assets/json")
        filepath = path.join(directory, filename)

        if not path.isdir(directory):
            makedirs(directory, exist_ok=True)

        f = open(filepath, "w")
        f.write(json)
        f.close()
