import math
import re

import nltk
from db.PostgresManager import PostgresManager
from util import clean

#  NLTK built-in support for dozens of corpora and trained models
nltk.download("punkt", quiet=True)


class Service:
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

    def __createVocabulary(self, sections):
        vocabulary = []

        for section in sections.values():
            lower = section.lower()
            only_letters = re.findall(r"[a-z]+", lower)
            new_section = " ".join(only_letters)
            tokens = nltk.word_tokenize(new_section)

            for token in tokens:
                if token not in vocabulary:
                    vocabulary.append(token)
        return vocabulary

    def __dictCount(self, vocabulary, section):
        dictCount = dict.fromkeys(vocabulary, 0)
        for word in section:
            dictCount[word] += 1
        return dictCount

    def __TF(self, dictCount, sectionTokens):
        tfDict = {}
        sectionWordCount = len(sectionTokens)

        for word, count in dictCount.items():
            tfDict[word] = count / float(sectionWordCount)

        return tfDict

    def __IDF(self, sections):
        idfDict = {}
        N = len(sections)

        for word in sections[0]:
            apparisionCount = 0
            for section in sections:
                if section[word] > 0:
                    apparisionCount += 1

            idfDict[word] = math.log10(N / apparisionCount)

        return idfDict

    def __TFIDF(self, tf_bow, idfs):
        tfidf = {}

        for word in tf_bow:
            tf = tf_bow[word]
            idf = idfs[word]
            tfidf[word] = tf * idf

        return tfidf

    def generateTFIDF(self):
        sections = self.getArticleSections()
        # PREPROCESSING?
        vocabulary: list[str] = self.__createVocabulary(sections)

        dictCount = {}
        tf_bows = {}
        tfidfs = {}

        for id, section in sections.items():
            lower = section.lower()
            only_letters = re.findall(r"[a-z]+", lower)
            new_section = " ".join(only_letters)
            tokens = nltk.word_tokenize(new_section)

            sectionDictCount = self.__dictCount(vocabulary, tokens)
            dictCount[id] = sectionDictCount

            tf = self.__TF(sectionDictCount, tokens)
            tf_bows[id] = tf

        idf = self.__IDF(list(dictCount.values()))

        for j in sections.keys():
            tfidfs[j] = self.__TFIDF(tf_bows[j], idf)

        print(tfidfs)
