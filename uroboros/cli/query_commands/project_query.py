# python3 -m uroboros.cli.query prj
# python3 -m uroboros.cli.query prj --json
# python3 -m uroboros.cli.query prj -f

import json
import pprint

from cli.query_commands.base_query import BaseQuery, time_decorator
from api.query_commands.project_query import ProjectApi


class ProjectQuery(BaseQuery):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper

    def run(self, args):
        try:
            proj = ProjectApi(self._db_helper)
            self.tbl_dict = proj.run(args.prj_id)
            if args.json:
                tbl = self.json_table()
                if args.f:
                    self.output_file(table=tbl)
                else:
                    pprint.pprint(json.loads(tbl))
            else:
                if args.f:
                    self.output_file()
                else:
                    self.str_table()
        except Exception as e:
            self._error(e)
