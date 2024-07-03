import argparse

from cli.baseapp import BaseApp
from cli.query_commands.assembly_query import AssemblyQuery
from cli.query_commands.changelog_query import ChangelogQuery
from cli.query_commands.cve_query import CveQuery
from cli.query_commands.package_query import PackageQuery
from cli.query_commands.project_query import ProjectQuery


def required_length(nmin, nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = 'argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest, nmin=nmin, nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(namespace, self.dest, values)

    return RequiredLength


class QueryUtility(BaseApp):
    def __init__(self):
        super().__init__()
        self._setup()

    def _setup(self):
        self._query_parser = self._parser.add_subparsers(title="query_commands",
                                                         description="tools for managing repository",
                                                         help="query", dest="command")

        # assembly
        self._assm_parser = self._query_parser.add_parser("assm", description="assembly queries",
                                                          help="assembly help")
        self._assm_parser.add_argument("--prj_id", type=int, action="store", default=None, help="project id")
        self._assm_parser.add_argument("--json", action="store_true", help="json output")
        self._assm_parser.add_argument('-f', action="store_true", help="output file")
        self._dict_command["assm"] = AssemblyQuery(self._db_helper)

        # project
        self._prj_parser = self._query_parser.add_parser("prj", description="project queries",
                                                         help="project help")
        self._prj_parser.add_argument("--prj_id", type=int, action="store", default=None, help="project id")
        self._prj_parser.add_argument("--json", action="store_true", help="json output")
        self._prj_parser.add_argument('-f', action="store_true", help="output file")
        self._dict_command["prj"] = ProjectQuery(self._db_helper)

        # package version
        self._pkg_parser = self._query_parser.add_parser("pkg", description="package query",
                                                         help="package help")
        self._pkg_parser.add_argument('--json', action="store_true", help="json output")
        self._pkg_parser.add_argument('-f', action="store_true", help="output file")
        self._pkg_parser.add_argument('--joint', action="store_true", help="get joint assembly")
        self._pkg_parser.add_argument('--difference', action="store_true", help="get difference assemblies")
        self._pkg_parser.add_argument('--delete', action="store_true", help="drop table")
        self._pkg_parser.add_argument('--dif_filter', type=str, nargs='+', action=required_length(1, 5),
                                      default=None, help="filter")
        self._pkg_parser.add_argument('--prev', action="store_true", help="check previous assembly")
        self._pkg_parser.add_argument('--current', action="store_true", help="check current assembly")
        self._pkg_parser.add_argument('--assm_id', type=int,
                                      default=None, help="assembly id")

        self._dict_command["pkg"] = PackageQuery(self._db_helper)

        # cve
        self._cve_parser = self._query_parser.add_parser("cve", description="cve query",
                                                         help="cve help")
        self._cve_parser.add_argument('--resolved', action="store_true", help="output resolved pkg_vrs_id")
        self._cve_parser.add_argument('--pkg_vrs_id', type=int, action="store", help="version of package id")
        self._cve_parser.add_argument('--assm_id', type=int, action="store", help="version of assm id")
        self._cve_parser.add_argument('--delete', action="store_true", help="delete table")
        self._cve_parser.add_argument('-f', action="store_true", help="output file")
        self._cve_parser.add_argument('--urgency', type=str, nargs='+', action=required_length(1, 8),
                                      default=None, help="status filter (open, resolved, undetermined)")
        self._cve_parser.add_argument("--joint", action="store_true")
        self._cve_parser.add_argument('--status', type=str, nargs='+', action=required_length(1, 3),
                                      default=None, )

        self._cve_parser.add_argument('--severity', type=str, nargs='+', action=required_length(1, 5),
                                      default=None, help="severity filter(Неизвестен, Низкий, Средний, Высокий, "
                                                         "Критический)")

        self._cve_parser.add_argument('--fdate', type=str, nargs='+', action=required_length(1, 3),
                                      default=None, help="start of time period")
        self._cve_parser.add_argument('--sdate', type=str, nargs='+', action=required_length(1, 3),
                                      default=None, help="end of time period")

        self._cve_parser.add_argument('--json', action="store_true", help="json output")

        self._dict_command["cve"] = CveQuery(self._db_helper)

        # changelog
        self._chng_parser = self._query_parser.add_parser("changelog", description="changelog query",
                                                          help="changelog help")
        self._chng_parser.add_argument('--pkg_vrs_id', type=int, action="store", help="version of package id")

        self._chng_parser.add_argument('-f', action="store_true", help="output file")

        self._chng_parser.add_argument('--json', action="store_true", help="json output")

        self._dict_command["changelog"] = ChangelogQuery(self._db_helper)

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
    upd = QueryUtility()
    upd.run()
