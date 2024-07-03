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


class BaseQuery(ABC):
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

    def _error(self, message):
        raise QueryError(message)

    @time_decorator
    def json_table(self):
        try:
            # return self.table_info
            return json.dumps(self.tbl_dict)
        except Exception as e:
            self._error(e)

    @time_decorator
    def str_table(self):
        try:
            for id_key in self.tbl_dict:
                print("\033[35m{}".format(id_key))
                print("\033[0m=================================================")
                if type(self.tbl_dict[id_key]) == list:
                    for value in self.tbl_dict[id_key]:
                        print(*value)
                        print("---------------------------------------")
                else:
                    for key, value in self.tbl_dict[id_key].items():
                        print("\033[32m{0}: \033[0m{1}".format(key, value))
                        print("---------------------------------------")
                print("=================================================")
        except Exception as e:
            self._error(e)

    @time_decorator
    def output_file(self, table=None):
        try:
            cmd = f'mkdir -p data'
            os.system(cmd)
            if table is not None:
                with open("data/table.txt", "w") as file:
                    file.write(table)
            else:
                with open("data/table.txt", "w") as file:
                    for id_key in self.tbl_dict:
                        file.write(" {}".format(id_key) + '\n')
                        file.write("=================================================" + "\n")
                        if type(self.tbl_dict[id_key]) == list:
                            for value in self.tbl_dict[id_key]:
                                file.write(*value)
                                file.write("\n")
                                file.write("---------------------------------------" + "\n")
                        else:
                            for key, value in self.tbl_dict[id_key].items():
                                file.write(" {0}: {1}".format(key, value) + "\n")
                                file.write("---------------------------------------" + "\n")
                        file.write("=================================================" + "\n")
        except Exception as e:
            self._error(e)

    @abstractmethod
    def run(self, args):
        pass
