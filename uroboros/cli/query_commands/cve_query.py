# python3 -m uroboros.cli.query cve
# python3 -m uroboros.cli.query cve --json
# python3 -m uroboros.cli.query cve -f
# python3 -m uroboros.cli.query cve --assm {--severity, --urgency, --status, --fdate, --sdate}
# python3 -m uroboros.cli.query cve --pkg_vrs {--fixed}

import json
import pprint

from uroboros.api.query_commands.cve_query import CveApi
from uroboros.cli.query_commands.base_query import BaseQuery, time_decorator


class CveQuery(BaseQuery):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper
        self.assm_id = None
        self.joint = False
        self.resolved = False
        self.pkg_vrs_id = None
        self.urgency = None
        self.severity = None
        self.status = None
        self.fdate = None
        self.sdate = None

    def run(self, args):
        try:
            self.assm_id = args.assm_id
            self.joint = args.joint
            self.resolved = args.resolved
            self.pkg_vrs_id = args.pkg_vrs_id
            self.urgency = args.urgency
            self.severity = args.severity
            self.status = args.status
            self.fdate = args.fdate
            self.sdate = args.sdate
            cve = CveApi(self._db_helper)
            self.tbl_dict = cve.run(self.__dict__)
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
        except Exception as e:
            self._error(e)
