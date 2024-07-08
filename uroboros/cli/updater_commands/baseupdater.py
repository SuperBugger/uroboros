import datetime
import os
from abc import ABC, abstractmethod
from datetime import datetime

from uroboros.cli.updater_commands.uptable import UpTableKeyed, UpTable


class UpdaterError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UpdaterError, this error is found while {} '.format(self.message)
        else:
            return 'UpdaterError'


class Updater(ABC):
    def __init__(self):
        super().__init__()
        self._uptables = dict()
        self.start_time = datetime.now()
        self._tmp_schema = None
        self._db_helper = None

    @abstractmethod
    def _download_obj(self, url):
        pass

    @abstractmethod
    def _get_data(self, path):
        pass

    @abstractmethod
    def run(self, no_clean, file, l):
        pass

    @abstractmethod
    def _clear_trash(self):
        pass

    def _merge_schemas(self):
        try:
            print(datetime.now(), "Schema merge..")
            sql = f"call maintenance.update_{self._tmp_schema}();"
            self._db_helper.query(sql)
            self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("merging {}".format(self._tmp_schema))

    def _error(self, message):
        raise UpdaterError(message)

    def _get_uptable(self, name):
        return self._uptables.get(name, None)

    def _ensure_uptable(self, name, fields, keyed=True):
        upt = self._uptables.get(name, None)
        if not upt:
            if keyed:
                upt = UpTableKeyed(self._db_helper, name, fields)
            else:
                upt = UpTable(self._db_helper, name, fields)
            self._uptables[name] = upt
        return upt

    def _delete_schema(self, name):
        try:
            print(datetime.now(), "Schema delete..")
            sql = f"DROP SCHEMA {name} CASCADE"
            self._db_helper.query(sql)
            self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("deleting {}".format(self._tmp_schema))

    def _create_temp_schema(self, name):
        self._tmp_schema = name
        try:
            sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = 'temp_{}'); ".format(self._tmp_schema)
            if self._db_helper.query(sql)[0][0]:
                self._delete_schema(f"temp_{self._tmp_schema}")
                self._db_helper.commit_conn()
            with open(os.path.join("scripts/templates", self._tmp_schema + ".sql"), 'r') as f:
                text = f.read()
                self._db_helper.query(text)
                self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("creating {}".format(self._tmp_schema))

    def _upload_tables(self):
        for n, t in self._uptables.items():
            print(datetime.now(), f"Import {t.name}")
            t.upload()
        self._db_helper.commit_conn()
        # self._db_helper.connect()

    def _add_fk(self):
        try:
            with open(os.path.join("scripts/schemas", "fk_{}.sql".format(self._tmp_schema)), 'r') as f:
                sql = f.read()
                print(datetime.now(), "Create fk for {} create".format(self._tmp_schema))
                self._db_helper.query(sql)
        except Exception as e:
            print(e)
            self._error("replacing {}".format(self._tmp_schema))

    def replace_schema(self, no_clean):
        try:
            print(datetime.now(), "Schema replace..")
            sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = 'old_{}'); ".format(self._tmp_schema)
            if self._db_helper.query(sql)[0][0]:
                self._delete_schema(f"old_{self._tmp_schema}")
            sql = f"ALTER SCHEMA {self._tmp_schema} RENAME TO old_{self._tmp_schema}"
            temp_sql = f"ALTER SCHEMA temp_{self._tmp_schema} RENAME TO {self._tmp_schema}"
            if not no_clean:
                sql = f"DROP SCHEMA {self._tmp_schema} CASCADE"
            self._db_helper.query(sql)
            self._db_helper.query(temp_sql)
            self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("replacing {}".format(self._tmp_schema))
