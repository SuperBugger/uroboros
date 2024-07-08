import sys

from uroboros.cli.baseapp import BaseApp
from uroboros.cli.updater_commands.bdu_updater import BduUpdater
from uroboros.cli.updater_commands.debtracker_updater import TrackerUpdater


class UpdaterUtility(BaseApp):
    def __init__(self):
        super().__init__()
        self._update_parser = None
        self._setup()

    def _setup(self):
        self._updater_parser = self._parser.add_subparsers(title="updater_commands", description="update debtracker "
                                                                                                 "and bdu commands",
                                                           help="update", dest="command")
        # debtracker command
        self._debtracker_parser = self._updater_parser.add_parser("debtracker",
                                                                  description="debtracker uploader commands",
                                                                  help="debtracker help")
        self._debtracker_parser.add_argument("--noclean", action="store_true", help="no clean data")
        self._debtracker_parser.add_argument("-f", dest="path", action="store", help="upload from file")
        self._debtracker_parser.add_argument("-u", action="store_true", help="upload from debtracker")
        self._dict_command["debtracker"] = TrackerUpdater(self._db_helper)
        # bdu command
        self._bdu_parser = self._updater_parser.add_parser("bdu", description="bdu commands",
                                                           help="bdu help")
        self._dict_command["bdu"] = BduUpdater(self._db_helper)
        self._bdu_parser.add_argument("--noclean", action="store_true", help="no clean data")
        self._bdu_parser.add_argument("-f", type=str, dest="path", action="store", default=None, help="upload from file")
        self._bdu_parser.add_argument("-u", action="store_true", help="upload from bdu fstek")

    def _execute(self):
        self._args = self._parser.parse_args()
        cmd = self._dict_command.get(self._args.command, None)
        if cmd:
            command = cmd
            try:
                if self._args.path is not None and self._args.u:
                    print("too many options")
                    sys.exit(1)
                if self._args.path is None and not self._args.u:
                    self._args.u = True
                command.run(self._args.noclean, self._args.path, self._args.u)
            except Exception as e:
                print(e)
        else:
            print("this command doesn't exist")


if __name__ == "__main__":
    upd = UpdaterUtility()
    upd.run()
