"""
python3 -m uroboros.cli.ctl initdb --force
"""

import os
import re

from ..ctl_commands.base_ctl_command import BaseCommand


class InitCommand(BaseCommand):
    def __init__(self, bd_helper):
        super().__init__()
        self._db_helper = bd_helper

    def run(self, args):
        # удаление схем
        if args.force:
            # проверка есть ли схемы. Если есть - удаляем
            for file in os.listdir("scripts/schemas"):
                if file.find('fk') != -1:
                    continue
                file = re.split("_", file)
                sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(file[1][:-4])
                if self._db_helper.query(sql)[0][0]:
                    self.delete_schema(file[1][:-4])
            for file in sorted(os.listdir("scripts/maintenance")):
                file = re.split("_", file)
                sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(file[1][:-4])
                if self._db_helper.query(sql)[0][0]:
                    self.delete_schema(file[1][:-4])
        self._create_schema()
        self._db_helper.commit_conn()

    def _create_schema(self):
        try:
            for file in sorted(os.listdir("scripts/schemas")):
                if file.find('fk') != -1:
                    continue
                with open(os.path.join("scripts/schemas", file), 'r') as f:
                    sql = f.read()
                    print("Schema from {} with tables create".format(f.name))
                    self._db_helper.query(sql)
            for file in sorted(os.listdir("scripts/maintenance")):
                with open(os.path.join("scripts/maintenance", file), 'r') as f:
                    sql = f.read()
                    print("Schema from {} with tables create".format(f.name))
                    self._db_helper.query(sql)
        except Exception as e:
            print(e)
            self._error("creating schema from {}.".format(f.name))
