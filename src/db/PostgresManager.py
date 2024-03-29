from os import environ, path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_batch


class PostgresManager:
    __conn = None

    def config(self):
        load_dotenv(dotenv_path=path.join(path.dirname(__file__), "..", "..", ".env"))
        db = [
            environ.get("HOST"),
            environ.get("DATABASE"),
            environ.get("UNAME"),
            environ.get("PASSWORD"),
        ]
        return db

    def __connect(self):
        params = self.config()
        self.__conn = psycopg2.connect(
            host=params[0], database=params[1], user=params[2], password=params[3]
        )

    def __cursor(self):
        self.__connect()
        return self.__conn.cursor()

    def __closeCursor(self):
        self.__conn.cursor().close()

    def __closeConn(self):
        self.__conn.close()

    def __commit(self):
        self.__conn.commit()

    def cursor(self):
        return self.__cursor()

    def insert(self, sql):
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute(sql)
            self.__commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()

    def insertAndReturnId(self, sql, tuple):
        id = None
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute(sql, tuple)
            id = cursor.fetchone()[0]
            self.__commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()
        return id

    def findOne(self, sql):
        rs = None
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute(sql)
            rs = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()
        return rs

    def fetchAll(self, sql):
        rs = None
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute(sql)
            rs = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()
        return rs

    def update(self, update, pair, tweets):
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute("PREPARE updateStmt AS " + update)
            execute_batch(cursor, "EXECUTE updateStmt " + pair, tweets, 100)
            cursor.execute("DEALLOCATE updateStmt")
            self.__commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()

    def delete(self, table, condition):
        try:
            self.__connect()
            cursor = self.__cursor()
            cursor.execute("DELETE FROM " + table + " WHERE " + condition)
            self.__commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__closeCursor()
                self.__closeConn()
