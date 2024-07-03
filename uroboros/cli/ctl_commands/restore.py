"""
python3 -m uroboros.cli.ctl restore <archive dir> --data-only --force
"""

import os
import re
import subprocess
import tarfile

from ..ctl_commands.base_ctl_command import BaseCommand
from uroboros.configure import USER_DB, PASSWORD_DB, HOST_DB, PORT_DB, NAME_DB


class RestoreCommand(BaseCommand):
    def __init__(self, bd_helper):
        super().__init__()
        self._db_helper = bd_helper
        self.cur_dir = os.path.abspath(os.curdir)

    @staticmethod
    def decompress_backup(path):
        print("Restore: Decompress backup")
        with tarfile.open(path, "r:gz") as tar:
            file_name = re.split(r"/", path)[-1]
            file_name = file_name[:-6] + "sql"
            member = tar.getmember(file_name)
            if member.isfile():
                tar.extract(member)
                return member.name

    def _restore(self, path, args):
        schema_name = ""

        for schm in ["debtracker", "bdu", "repository", "maintenance", "db"]:
            if path.find(schm) != -1:
                schema_name = schm
                break
        if len(schema_name) == 0:
            self._error("schema not found")
            exit(1)
        print("Restore: {} successful found".format(schema_name))
        try:
            command = "python3 -m cli.ctl clean --{}".format(schema_name)
            if schema_name == "db":
                command = "python3 -m cli.ctl clean --{}".format("all")
            if args.force:
                command += " --force"
            if args.data_only:
                if schema_name != "db":
                    sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(schema_name)
                    if not self._db_helper.query(sql)[0][0]:
                        self._error("Backup: Schema doesn't exist")
                        exit(1)
                else:
                    sql = "SELECT EXISTS(SELECT * FROM pg_database WHERE datname = 'uroboros');"
                    if not self._db_helper.query(sql)[0][0]:
                        self._error("Backup: Database doesn't exist")
                        exit(1)
                os.system(command)
            else:
                if schema_name == "db":
                    for schm in ['debtracker', 'bdu', 'maintenance', 'repository']:
                        self.delete_schema(schm)
                else:
                    self.delete_schema(schema_name)

            pg_command = ['psql', 'pg_restore']
            path = self.decompress_backup(path)
            pg_command += ['--dbname=postgresql://{}:{}@{}:{}/{}'.format(USER_DB,
                                                                         PASSWORD_DB,
                                                                         HOST_DB,
                                                                         PORT_DB, NAME_DB), "-f", path]
            if args.data_only:
                pg_command += ["-a"]
            else:
                if schema_name == "db":
                    sql = "SELECT EXISTS(SELECT * FROM pg_database WHERE datname = 'uroboros');"
                    if not self._db_helper.query(sql)[0][0]:
                        sql = "CREATE DATABASE uroboros;"
                        self._db_helper.query(sql)
                    for schm in ["debtracker", "bdu", "repository", "maintenance", "db"]:
                        sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(schm)
                        if self._db_helper.query(sql)[0][0]:
                            self._error("schema exist")
                            exit(1)
                else:
                    sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(schema_name)
                    if self._db_helper.query(sql)[0][0]:
                        self._error("schema exist")
                        exit(1)

            process = subprocess.Popen(
                pg_command,
                stdout=subprocess.PIPE
            )
            process.wait()
            if process.returncode != 0 and process.returncode is not None:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
            print("{} is successful restoring".format(schema_name))
            path = re.split(r"/", path)[-1]
            self.delete_backup_file(path)
        except Exception as e:
            print(e)
            self._error("restoring {}".format(schema_name))

    def run(self, args):
        path = ""
        super().run(args)
        try:
            dump_paths = re.split(r" ", args.path)
            for path in dump_paths:
                print("Start restore from {} file".format(path))
                self._restore(path, args)
        except Exception as e:
            print(e)
            self._error("restoring {}".format(path))
