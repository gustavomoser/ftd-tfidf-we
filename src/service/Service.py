from db.PostgresManager import PostgresManager

class Service: 
  def saveTweets(self, tweets):
    pm = PostgresManager()
    insert = ','.join(pm.cursor().mogrify("(%s,%s)", (tweet['id'], tweet['text'])).decode('utf-8') for tweet in tweets)
    pm.insert("INSERT INTO tweet (id, tweet) VALUES " + insert + " ON CONFLICT DO NOTHING;")

  def saveArticles(self, articles):
    pm = PostgresManager()
    for article in articles:
      title = article['title']
      exists = pm.findOne('SELECT 1 FROM article WHERE title = \'{}\';'.format(title))
      if exists is None: 
        id = pm.insertAndReturnId("INSERT INTO article (title) VALUES (%s) RETURNING id;", (title,))

        authors_list = article['authors']
        authors = ','.join(pm.cursor().mogrify("(%s,%s)", (id, author)).decode('utf-8') for author in authors_list)
        pm.insert("INSERT INTO author (article_id, name) VALUES " + authors + ";")

        section_list = article['sections']
        sections = ','.join(pm.cursor().mogrify("(%s,%s,%s)", (id, section['section'], section['content'].replace("'", "''"))).decode('utf-8') for section in section_list)
        pm.insert("INSERT INTO article_section (id, title, content) VALUES " + sections + ";")





      




