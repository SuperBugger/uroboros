import argparse
from uroboros.configure import *
from uroboros.connection import DbHelper


class BaseApp(object):
    def __init__(self):
        self._db_helper = DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB)
        self._dict_command = {}
        self._parser = argparse.ArgumentParser(description='Uroboros')

    def _execute(self):
        pass

    def run(self):
        try:
            self._execute()
        except Exception as e:
            raise e

    def _setup(self):
        self._parser.add_argument("-v", "--verbose")
        self._parser.add_argument("-d", "--debug")
        self._parser.add_argument('--syslog')
        self._parser.add_argument("--version")


if __name__ == "__main__":
    pass
