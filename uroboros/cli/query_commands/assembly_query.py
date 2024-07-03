# python3 -m uroboros.cli.query assm
# python3 -m uroboros.cli.query assm --json
# python3 -m uroboros.cli.query assm -f

import json
import pprint

from api.query_commands.assembly_query import AssemblyApi
from cli.query_commands.base_query import BaseQuery


class AssemblyQuery(BaseQuery):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper

    def run(self, args):
        try:
            assm = AssemblyApi(self._db_helper)
            self.tbl_dict = assm.run(args.prj_id)
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
