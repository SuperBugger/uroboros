# python3 -m uroboros.cli.query changelog --pkg_vrs_id
# python3 -m uroboros.cli.query changelog --json
# python3 -m uroboros.cli.query changelog -f

import json
import pprint

from uroboros.api.query_commands.changelog_query import ChangelogApi
from uroboros.cli.query_commands.base_query import BaseQuery


class ChangelogQuery(BaseQuery):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper
        self.pkg_vrs_id = None

    def run(self, args):
        self.pkg_vrs_id = args.pkg_vrs_id
        chng = ChangelogApi(self._db_helper)
        self.tbl_dict = chng.run(self.__dict__)
        if args.json:
            tbl = self.json_table()
            if args.f:
                self.output_file(tbl)
            else:
                pprint.pprint(json.loads(tbl))
        else:
            if args.f:
                self.output_file()
            else:
                self.str_table()
