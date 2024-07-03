"""
python3 -m uroboros.cli.ctl clean --bdu
python3 -m uroboros.cli.ctl clean --debtracker
python3 -m uroboros.cli.ctl clean --rep
python3 -m uroboros.cli.ctl clean --maintenance
python3 -m uroboros.cli.ctl clean --db
python3 -m uroboros.cli.ctl clean --bdu --force
"""

import os
import re

from ..ctl_commands.base_ctl_command import BaseCommand


class CleanCommand(BaseCommand):
    def __init__(self, bd_helper):
        super().__init__()
        self._db_helper = bd_helper

    def cleaning(self, schema_name, args):
        try:
            if schema_name == "db":
                sql = "SELECT EXISTS(SELECT * FROM pg_database WHERE datname = 'uroboros');"
                if self._db_helper.query(sql)[0][0]:
                    if not args.force:
                        print("Cleaning: Create backup for {}".format(schema_name))
                        command = "python3 -m cli.ctl backup --{}".format("all")
                        command += " --data-only"
                        os.system(command)
                else:
                    print("Cleaning: DB doesn't exist")
                    exit(1)
            else:
                sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(schema_name)
                if self._db_helper.query(sql)[0][0]:
                    if not args.force:
                        print("Cleaning: Create backup for {}".format(schema_name))
                        command = "python3 -m cli.ctl backup --{}".format(schema_name)
                        command += " --data-only"
                        os.system(command)
                else:
                    print("Cleaning: Schema doesn't exist")
                    exit(1)

            if schema_name != "db":
                print("Cleaning: Drop schema: {}".format(schema_name))
                self.delete_schema(schema_name)
            else:
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

            name = ""
            if schema_name != "db":
                for schm in os.listdir("scripts/schemas"):
                    if schm.find(schema_name) != -1 and schm.find("fk") == -1:
                        name = schm
                        break
                if len(name) == 0:
                    self._error("Cleaning: schema not found")
                with open("scripts/schemas/{}".format(name), 'r') as f:
                    sql = f.read()
                    print("Cleaning: Schema from {} with tables create".format(f.name))
                    self._db_helper.query(sql)
            else:
                command = "python3 -m cli.ctl initdb --force"
                os.system(command)
            self._db_helper.commit_conn()
            print("Cleaning: Successful clean")

        except Exception as e:
            print(e)
            self._error("Cleaning: creating schema from {}.".format(schema_name))

    def run(self, arg):
        schm = ""
        try:
            if arg.bdu:
                schm = "bdu"
                print("Start clean {}".format(schm))
                self.cleaning(schm, arg)
            if arg.debtracker:
                schm = "debtracker"
                print("Start clean {}".format(schm))
                self.cleaning(schm, arg)
            if arg.rep:
                print("Start clean {}".format(schm))
                schm = "repository"
                self.cleaning(schm, arg)
            if arg.maintenance:
                print("Start clean {}".format(schm))
                schm = "maintenance"
                self.cleaning(schm, arg)
            if arg.all:
                schm = "db"
                print("Start clean {}".format(schm))
                self.cleaning(schm, arg)
        except Exception as e:
            print(e)
            self._error("creating schema from {}.".format(schm))
