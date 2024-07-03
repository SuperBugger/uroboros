import json
import os
from abc import ABC, abstractmethod
from datetime import datetime


def time_decorator(function_to_decorate):
    def the_wrapper_around_the_original_function(*args, **kwargs):
        print(datetime.now(), f"while {function_to_decorate.__name__}")
        return function_to_decorate(*args, **kwargs)

    return the_wrapper_around_the_original_function


class QueryError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'QueryError, this error is found while {} '.format(self.message)
        else:
            return 'QueryError'


class BaseApi(ABC):
    def __init__(self):
        super().__init__()
        self.tbl_dict = dict()
        self._db_helper = None
        self.table_name = ""
        self.fields = ""
        self.name_col = ""
        self.where = " where "
        self.join = ""
        self.query = ""

    @time_decorator
    def create_query(self, tbl_id):
        pass

    def _error(self, message):
        raise QueryError(message)

    @time_decorator
    def run_query(self, build=True, t_id=True):
        try:
            if build:
                self.query = f"select {self.fields} from {self.table_name}"
                if len(self.join) != 0:
                    self.query += self.join
                if len(self.where) != 0:
                    self.query += self.where
            table_info = self._db_helper.query(self.query)
            count = 0
            if len(table_info) != 0:
                for sttr in table_info:
                    if not t_id:
                        count += 1
                        self.tbl_dict[count] = {}
                        for i in range(0, len(self.name_col)):
                            self.tbl_dict[count][self.name_col[i]] = str(sttr[i])
                    else:
                        self.tbl_dict[sttr[0]] = {}
                        for i in range(1, len(self.name_col)):
                            self.tbl_dict[sttr[0]][self.name_col[i]] = str(sttr[i])

        except Exception as e:
            self._error(e)

    @abstractmethod
    def run(self, args):
        pass
