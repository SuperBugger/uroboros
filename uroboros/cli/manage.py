import argparse

from cli.baseapp import BaseApp
from cli.manage_commands.assembly_uploader import AssemblyUploader
from cli.manage_commands.changelog_parser import ChangelogUploader
from cli.manage_commands.pkg_uploader import PkgUploader
from cli.manage_commands.project_uploader import ProjectUploader


def required_length(nmin, nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = 'argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest, nmin=nmin, nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(namespace, self.dest, values)

    return RequiredLength


class ManageUtility(BaseApp):
    def __init__(self):
        super().__init__()
        self._update_parser = None
        self._setup()


    def _setup(self):
        self._manage_parser = self._parser.add_subparsers(title="manage_repository_commands",
                                                          description="tools for managing repository",
                                                          help="manage", dest="command")
        # rep command
        self._assm_parser = self._manage_parser.add_parser("assm",  description="managing assemblies",
                                                           help="assembly help")
        self._assm_parser.add_argument("-r", action="store_true", help="getting from remote repository")
        self._assm_parser.add_argument("-l", action="store_true", help="getting from local repository")
        self._assm_parser.add_argument("--path", type=str, action="store",
                                       help="path of repository for getting information about assembly")
        self._assm_parser.add_argument("--deb", action="store_true", help="upload only deb packages")
        self._assm_parser.add_argument('--pkg', action="store_true", help="getting information about packages "
                                                                          "from archives and files")
        self._assm_parser.add_argument("--noclean", action="store_true", help="no clean data")
        self._assm_parser.add_argument("--project", type=int, action="store", default=None, help="project id")
        self._assm_parser.add_argument("--date_created", type=str, nargs='+', action=required_length(1, 3),
                                       default=None,
                                       help="date added")
        self._assm_parser.add_argument("--delete", type=int, default=None, action="store",
                                      help="delete assembly")
        self._dict_command["assm"] = AssemblyUploader(self._db_helper)

        # prj command
        self._prj_parser = self._manage_parser.add_parser("prj", description="managing projects",
                                                          help="project help")
        self._prj_parser.add_argument("--noclean", action="store_true", help="no clean data")
        self._prj_parser.add_argument('-l', action="store_true", default=None,
                                      help="upload project from local repository")
        self._prj_parser.add_argument('--input', action="store_true", help="input command for adding project")
        self._prj_parser.add_argument("--path", type=str, action="store", default=None,
                                      help="path for getting from local repository")
        self._prj_parser.add_argument("--delete", type=int, default=None, action="store",
                                      help="delete project")
        self._dict_command["prj"] = ProjectUploader(self._db_helper)

        self._pkg_parser = self._manage_parser.add_parser("pkg", description="managing package",
                                                          help="package help")
        self._pkg_parser.add_argument("--noclean", action="store_true", help="co clean data")
        self._pkg_parser.add_argument("--path", action="store", default=None,
                                      help="path for adding packages")
        self._pkg_parser.add_argument('-l', action="store_true", help="getting data form local repository")
        self._pkg_parser.add_argument('-r', action="store_true", help="getting data form remote repository")
        self._pkg_parser.add_argument('--deb', action="store_true", help="getting only deb packages")
        self._pkg_parser.add_argument('--pkg', action="store_true", help="getting information about packages "
                                                                         "from archives and files")
        self._pkg_parser.add_argument('--assembly', type=int, action="store", help="assembly id")

        self._dict_command["pkg"] = PkgUploader(self._db_helper)

        self._log_parser = self._manage_parser.add_parser("changelog", description="managing changelog",
                                                          help="changelog help")
        self._log_parser.add_argument("--noclean", action="store_true", help="input command")
        self._log_parser.add_argument('-l', type=str, action="store", help="input command")

        self._dict_command["changelog"] = ChangelogUploader(self._db_helper)

    def _execute(self):
        self._args = self._parser.parse_args()
        cmd = self._dict_command.get(self._args.command, None)
        if cmd:
            command = cmd
            try:
                command.run(self._args)
            except Exception as e:
                print(e)
        else:
            print("this command doesn't exist")


if __name__ == "__main__":
    upd = ManageUtility()
    upd.run()
