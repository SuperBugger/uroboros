from uroboros.cli.baseapp import BaseApp
from uroboros.cli.ctl_commands.backup import BackupCommand
from uroboros.cli.ctl_commands.cleansing import CleanCommand
from uroboros.cli.ctl_commands.initdb import InitCommand
from uroboros.cli.ctl_commands.restore import RestoreCommand


class CtlUtility(BaseApp):
    def __init__(self):
        super().__init__()
        self._ctl_parser = None
        self._args = None
        self._setup()

    def _execute(self):
        self._args = self._parser.parse_args()
        cmd = self._dict_command.get(self._args.command, None)
        if cmd:
            try:
                command = cmd
                if isinstance(command, RestoreCommand):
                    if self._args.path is None:
                        print("didn't enter the path to the backup file")
                        exit(1)
                if isinstance(command, CleanCommand) or isinstance(command, BackupCommand):
                    if not self._args.bdu:
                        if not self._args.debtracker:
                            if not self._args.maintenance:
                                if not self._args.rep:
                                    if not self._args.all:
                                        print("missing parameters")
                                        exit(1)
                command.run(self._args)
            except Exception as e:
                print(e)
        else:
            print("this command doesn't exist")

    def _setup(self):
        super()._setup()
        self._ctl_parser = self._parser.add_subparsers(title="commands", description="ctl commands",
                                                       help="commands to initialize, clean up, "
                                                            "and manipulate schema and database copies", dest="command")
        # init command
        self._initdb_parser = self._ctl_parser.add_parser("initdb", prog='initdb', description="initdb commands",
                                                          usage='%(prog)s [options]', help="Database "
                                                                                           "initialization."
                                                                                           "Creating diagrams")
        self._initdb_parser.add_argument("--force", action="store_true", help="delete old schemas")

        self._backup_parser = self._ctl_parser.add_parser("backup", prog="backup", description="backup command",
                                                          usage='%(prog)s [options]', help="Schema and database backup")
        self._backup_parser.add_argument("--bdu", action="store_true", help="bdu backup")
        self._backup_parser.add_argument("--debtracker", action="store_true", help="debtracker backup")
        self._backup_parser.add_argument("--rep", action="store_true", help="repository backup")
        self._backup_parser.add_argument("--maintenance", action="store_true", help="maintenance backup")
        self._backup_parser.add_argument("--all", action="store_true", help="database backup")
        # self._backup_parser.add_argument("--force", action="store_true", help="delete")
        self._backup_parser.add_argument("--data-only", dest="data_only", action="store_true",
                                         help="save data without structure of "
                                              "schema")

        self._restore_parser = self._ctl_parser.add_parser("restore", prog="restore", description="restore command",
                                                           help="Restoring schematic and database copies",
                                                           usage='%(prog)s [options]')
        self._restore_parser.add_argument("path", action="store", help="add backup path", default=None)
        self._restore_parser.add_argument("--force", action="store_true", help="delete old data from schema or database")
        self._restore_parser.add_argument("--data-only", dest="data_only", action="store_true", help="restore data "
                                                                                                     "without "
                                                                                                     "structure of"
                                                                                                     "schema")

        self._clean_parser = self._ctl_parser.add_parser("clean",  prog="restore", description="clean command",
                                                         help="restoring backups of schemas and database",
                                                         usage='%(prog)s [options]')
        self._clean_parser.add_argument("--bdu", action="store_true", help="restoring bdu schema")
        self._clean_parser.add_argument("--debtracker", action="store_true", help="restoring debtracker schema")
        self._clean_parser.add_argument("--rep", action="store_true", help=" restoring repository schema")
        self._clean_parser.add_argument("--maintenance", action="store_true", help=" restoring maintenance schema")
        self._clean_parser.add_argument("--all", action="store_true", help="restoring database")
        self._clean_parser.add_argument("--force", action="store_true", help="delete schema or database without "
                                                                             "create backups")

        self._dict_command["initdb"] = InitCommand(self._db_helper)
        self._dict_command["backup"] = BackupCommand(self._db_helper)
        self._dict_command["restore"] = RestoreCommand(self._db_helper)
        self._dict_command["clean"] = CleanCommand(self._db_helper)


if __name__ == "__main__":
    ctl = CtlUtility()
    ctl.run()
