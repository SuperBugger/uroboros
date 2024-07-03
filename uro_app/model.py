import json
import os
import subprocess

from uroboros.api.query_commands.assembly_query import AssemblyApi
from uroboros.api.query_commands.changelog_query import ChangelogApi
from uroboros.api.query_commands.cve_query import CveApi
from uroboros.api.query_commands.package_query import PackageApi
from uroboros.api.query_commands.project_query import ProjectApi
from uroboros.configure import NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB
from uroboros.connection import DbHelper


class Column(object):
    def __init__(self, type_column, pk=False, fk=None):
        self.type_column = type_column
        self.primary_key = pk
        self.fk_ref = fk


class Base(object):
    def __init__(self):
        self._db_helper = DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB)

    def get_data(self):
        with open('data/table.txt') as f:
            return f.read()

    def command_s(self, command):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE
        )
        process.wait()


class Project(Base):
    def __init__(self):
        super().__init__()
        self.prj = ProjectApi(self._db_helper)
        self.command = None

    def get_prj(self):
        return self.prj.run(None)

    def add_prj_input(self, prj_name=None, rel_name=None, arch_name=None, prj_desc=None, vendor=None):
        self.command = "python3 -m uroboros.cli.manage prj --input"

    def add_prj_path(self, path):
        self.command = f"python3 -m uroboros.cli.manage prj -l --path {path}"

    def delete_prj(self, prj_id):
        self.command = f"python3 -m uroboros.cli.manage prj --delete --project {prj_id}"


class Assembly(Base):
    def __init__(self):
        super().__init__()
        self.assm = AssemblyApi(self._db_helper)
        self.command = None

    def get_assm(self, prj_id):
        return self.assm.run(prj_id)


class Package(Base):
    def __init__(self, assm_id=None, difference=False, delete=False, joint=False, prev=False, current=False,
                 dif_filter=None):
        super().__init__()
        self.assm_id = assm_id
        self.difference = difference
        self.delete = delete
        self.joint = joint
        self.prev = prev
        self.current = current
        self.dif_filter = dif_filter
        self.command = None
        self.pkg = PackageApi(self._db_helper)

    def get_pkg(self):
        print('sssssssssssss')
        return self.pkg.run(self.__dict__)


# TODO +RESOLVED AND FILTER

class Vulnerability(Base):
    def __init__(self, assm_id=None, joint=False, resolved=False, pkg_vrs_id=None,
                 urgency=None, severity=None, status=None, fdate=None, sdate=None):
        super().__init__()
        self.assm_id = assm_id
        self.joint = joint
        self.resolved = resolved
        self.pkg_vrs_id = pkg_vrs_id
        self.urgency = urgency
        self.severity = severity
        self.status = status
        self.fdate = fdate
        self.sdate = sdate
        self.command = None
        self.cve = CveApi(self._db_helper)

    def get_cve(self):
        print(self.__dict__)
        return self.cve.run(self)


class Changelog(Base):
    def __init__(self, pkg_vrs_id):
        super().__init__()
        self.pkg_vrs_id = pkg_vrs_id
        self.chng = ChangelogApi(self._db_helper)

    def get_chng(self):
        return self.chng.run(self.__dict__)

