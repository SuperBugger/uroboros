import re

import psycopg2
from psycopg2 import OperationalError


class DbHelper(object):
    def __init__(self, db_name, user, password, host, port):
        self._connection = None
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._cursor = None
        self._db_name = db_name
        self.connect()

    def query(self, sql):
        self._cursor = self._connection.cursor()
        try:
            if type(sql) == str:
                self._cursor.execute(sql)
                if re.search(r"select", sql.lower()) and not sql.lower().startswith("create"):
                    result = self._cursor.fetchall()
                    return result
            else:
                self._cursor.execute(sql[0], sql[1])
                if re.search(r"SELECT", sql[0]) and not sql[0].lower().startswith("create"):
                    result = self._cursor.fetchall()
                    return result
        except psycopg2.ProgrammingError as e:
            raise e

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                database=self._db_name,
                user=self._user,
                password=self._password,
                host=self._host,
                port=self._port,
            )
            print("Connection to PostgreSQL DB successful")
            return self._connection
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return None

    def commit_conn(self, end_status=False):
        self._cursor.close()
        self._connection.commit()
        if end_status:
            self._connection.close()
