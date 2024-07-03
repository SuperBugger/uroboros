# python3 -m uroboros.cli.ctl backup --deb
# python3 -m uroboros.cli.ctl backup --rep
# python3 -m uroboros.cli.ctl backup --bdu
# python3 -m uroboros.cli.ctl backup --db --data_only

import re
import subprocess
import tarfile
from datetime import datetime
import os
from ..ctl_commands.base_ctl_command import BaseCommand
from uroboros.configure import USER_DB, PASSWORD_DB, HOST_DB, NAME_DB, PORT_DB


class BackupCommand(BaseCommand):
    def __init__(self, bd_helper):
        super().__init__()
        self._db_helper = bd_helper
        self._force = False
        self.cur_dir = os.path.abspath(os.curdir)

    @staticmethod
    def compress_backup(path):
        with tarfile.open("{}.tar.gz".format(path[:-4]), "w:gz") as tar:
            file = open(path, "r")
            name = re.split(r"/", path)[-1]
            file_to_arch = open(name, "w")
            file_to_arch.write(file.read())
            tar.add(file_to_arch.name)
            os.remove(path)
            os.remove(re.split(r"/", path)[-1])
            print("Backup: Compress backup")

    @staticmethod
    def create_backup_file(schema_name, only_data):
        if only_data:
            if not os.path.exists(f"backups/{schema_name}/only_data"):
                if not os.path.exists(f"backups/{schema_name}"):
                    if not os.path.exists("backups"):
                        print("Backup: Create backups dir".format())
                        os.mkdir("backups")
                    print("Backup: Create {} dir".format(schema_name))
                    os.mkdir(f"backups/{schema_name}")
                print("Backup: Create {} dir".format("only_data"))
                os.mkdir(f"backups/{schema_name}/only_data")
        else:
            if not os.path.exists(f"backups/{schema_name}/struct_and_data"):
                if not os.path.exists(f"backups/{schema_name}"):
                    if not os.path.exists("backups"):
                        print("Backup: Create backups dir".format())
                        os.mkdir("backups")
                    print("Backup: Create {} dir".format(schema_name))
                    os.mkdir(f"backups/{schema_name}")
                print("Backup: Create {} dir".format("struct_and_data"))
                os.mkdir(f"backups/{schema_name}/struct_and_data")

        cur_time = datetime.now()
        file_name = "backups/{}/struct_and_data/{}.sql".format(schema_name,
                                                               "{}_{}".format(cur_time.strftime("%m.%d.%Y_%H:%M:%S"),
                                                                              schema_name))
        if only_data:
            file_name = "backups/{}/only_data/{}.sql".format(schema_name,
                                                             "{}_{}".format(cur_time.strftime("%m.%d.%Y_%H:%M:%S"),
                                                                            schema_name))
        return file_name

    def backup(self, name, args):
        try:
            if name != "db":
                sql = "SELECT EXISTS(SELECT * FROM pg_tables WHERE schemaname = '{}'); ".format(name)
                if not self._db_helper.query(sql)[0][0]:
                    self._error("Backup: Schema doesn't exist")
                    exit(1)
            else:
                sql = "SELECT EXISTS(SELECT * FROM pg_database WHERE datname = 'uroboros');"
                if not self._db_helper.query(sql)[0][0]:
                    self._error("Backup: Database doesn't exist")
            file_name = self.create_backup_file(name, args.data_only)
            pg_command = ['pg_dump',
                          '--dbname=postgresql://{}:{}@{}:{}/{}'.format(USER_DB, PASSWORD_DB, HOST_DB, PORT_DB,
                                                                        NAME_DB),
                          "-f", file_name]
            if args.data_only:
                pg_command += ["--data-only"]
            if name != "db":
                pg_command += "-n", name
            process = subprocess.Popen(pg_command)
            process.wait()
            print("Backup: Successful backup".format(name))
            self.compress_backup(file_name)
            if process.returncode != 0 and process.returncode is not None:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
        except Exception as e:
            print(e)
            self._error("Backup: backup {} schema.".format(name))

    def run(self, args):
        schm = ""
        try:
            if args.bdu:
                schm = "bdu"
                print("Backup {}".format(schm))
                self.backup(schm, args)
            if args.debtracker:
                schm = "debtracker"
                print("Backup {}".format(schm))
                self.backup(schm, args)
            if args.rep:
                schm = "repository"
                print("Backup {}".format(schm))
                self.backup(schm, args)
            if args.maintenance:
                schm = "maintenance"
                print("Backup {}".format(schm))
                self.backup(schm, args)
            if args.all:
                schm = "db"
                print("Backup {}".format("db"))
                self.backup("db", args)
        except Exception as e:
            print(e)
            self._error("backup {}.".format(schm))
