# python3 -m uroboros.cli.query pkg
# python3 -m uroboros.cli.query pkg --json
# python3 -m uroboros.cli.query pkg -f
# python3 -m uroboros.cli.query pkg assm_id

import json
import pprint

from api.query_commands.package_query import PackageApi
from cli.query_commands.base_query import BaseQuery, time_decorator


# pkg_vrs_id and date
class PackageQuery(BaseQuery):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper
        self.assm_id = None
        self.difference = False
        self.delete = False
        self.joint = False
        self.prev = False
        self.current = False
        self.dif_filter = None

    def run(self, args):
        try:
            pkg = PackageApi(self._db_helper)
            self.assm_id = args.assm_id
            self.difference = args.difference
            self.delete = args.delete
            self.joint = args.joint
            self.prev = args.prev
            self.current = args.current
            self.dif_filter = args.dif_filter
            self.tbl_dict = pkg.run(self)
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
