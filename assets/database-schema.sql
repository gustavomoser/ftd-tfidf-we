CREATE TABLE TWEET (
	id BIGINT,
	tweet TEXT NOT NULL,
	CONSTRAINT PK_TWEET_ID PRIMARY KEY (id)	
);

CREATE TABLE TWEET_CLEAN (
	id BIGINT,
	tweet TEXT NOT NULL,
	CONSTRAINT PK_TWEET_ID PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES TWEET (id)	
);

CREATE TABLE ARTICLE (
	id SERIAL,
	title VARCHAR NOT NULL,
	CONSTRAINT PK__ARTICLE_ID PRIMARY KEY (id)
);

CREATE TABLE AUTHOR (
	id SERIAL,
	article_id INT,
	name VARCHAR NOT NULL,
	CONSTRAINT PK_AUTHOR_ID PRIMARY KEY (id),
	FOREIGN KEY (article_id) REFERENCES ARTICLE (id)
);

CREATE TABLE ARTICLE_SECTION (
	id SERIAL,
	title VARCHAR NOT NULL,
	content TEXT NOT NULL,
	CONSTRAINT PK_SESSION_ID PRIMARY KEY (id, title)
);

