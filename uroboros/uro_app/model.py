import json
import os
import subprocess

from uroboros.api.manage_commands.assembly_uploader import AssemblyUploaderApi
from uroboros.api.manage_commands.project_uploader import ProjectUploaderApi
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
        self.db_helper = DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB)

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
        self.prj = ProjectApi(self.db_helper)
        self.command = None
        self.prj_name = None
        self.rel_name = None
        self.prj_desc = None
        self.vendor = None
        self.arch_name = None
        self.input = False
        self.l = False
        self.delete = None
        self.noclean = False

    def get_prj(self):
        return self.prj.run(None)

    def add_prj_input(self):
        prj = ProjectUploaderApi(self.db_helper)
        if prj.run(self):
            return True
        else:
            return False

    def add_prj_path(self):
        prj = ProjectUploaderApi(self.db_helper)
        return prj.run(self)

    def delete_prj(self):
        prj = ProjectUploaderApi(self.db_helper)
        return prj.run(self)


class Assembly(Base):
    def __init__(self):
        super().__init__()
        self.command = None
        self.prj_id = None
        self.delete = None
        self.date_created = None
        self.project = None
        self.deb = False
        self.pkg = False
        self.l = False
        self.r = False
        self.path = None
        self.noclean = False

    def get_assm(self, prj_id):
        assm = AssemblyApi(self.db_helper)
        return assm.run(prj_id)

    def add_assm(self):
        assm = AssemblyUploaderApi(self.db_helper)
        return assm.run(self)

    def delete_assm(self):
        assm = AssemblyUploaderApi(self.db_helper)
        return assm.run(self)


class Package(Base):
    def __init__(self):
        super().__init__()
        self.assm_id = None
        self.difference = False
        self.prev = False
        self.current = False
        self.joint = False
        self.delete = False
        self.dif_filter = []

    def check_delete(self):
        pkg = PackageApi(self.db_helper)
        pkg.delete_table("assm_vul")
        pkg.delete_table('compare_assm')

    def get_pkg(self, assm_id):
        pkg = PackageApi(self.db_helper)
        self.assm_id = assm_id
        return pkg.run(self)

    def get_joint_assm(self):
        pkg = PackageApi(self.db_helper)
        self.joint = True
        return pkg.run(self)

    def get_compare_assm(self):
        self.difference = True
        pkg = PackageApi(self.db_helper)
        return pkg.run(self)


# TODO +RESOLVED AND FILTER

class Vulnerability(Base):
    def __init__(self):
        super().__init__()
        self.pkg_vrs_id = None
        self.pkg_vul_id = None
        self.assm_id = None
        self.resolved = False
        self.joint = False
        self.delete = False
        self.urgency = None
        self.status = None
        self.severity = None
        self.fdate = None
        self.sdate = None

    def filters(self, filter_list):

        st = []
        print(filter_list)
        if 'undetermined' in filter_list:
            st.append("undetermined")
        elif 'open' in filter_list:
            st.append("open")
        elif 'resolved' in filter_list:
            st.append("resolved")

        urg = []
        if 'unimportant' in filter_list:
            urg.append("unimportant")
        elif 'low' in filter_list:
            urg.append("low")
        elif 'end-of-life' in filter_list:
            urg.append("end-of-life")
        elif 'medium' in filter_list:
            urg.append("medium")
        elif 'high' in filter_list:
            urg.append("high")

        sev = []
        if 'Неизвестен' in filter_list:
            sev.append("Неизвестен")
        elif 'Низкий' in filter_list:
            sev.append("Низкий")
        elif 'Средний' in filter_list:
            sev.append("Средний")
        elif 'Высокий' in filter_list:
            sev.append("Высокий")
        elif 'Критический' in filter_list:
            sev.append("Критический")

        if filter_list['current'] != '':
            self.fdate = filter_list['current']
        if filter_list['current'] != '':
            self.sdate = filter_list['prev']

        if len(urg)!=0:
            self.urgency = urg
        if len(st)!=0:
            self.status = st
        if len(sev)!=0:
            self.severity = sev
        print(self.urgency)
        print(self.status)
        print(self.severity)

    def get_pkg_cve(self, fil_list=None):
        if fil_list is not None:
            self.filters(fil_list)
        cve = CveApi(self.db_helper)
        return cve.run(self)

    def get_assm_cve(self, fil_list=None):
        if fil_list is not None:
            self.filters(fil_list)
        cve = CveApi(self.db_helper)
        return cve.run(self)

    def get_joint_assm_cve(self, fil_list=None):
        self.joint = True
        if fil_list is not None:
            self.filters(fil_list)
        cve = CveApi(self.db_helper)
        return cve.run(self)


class Changelog(Base):
    def __init__(self):
        super().__init__()
        self.command = None
        self.pkg_id = None

    def get_chng(self):
        chng_log = ChangelogApi(self.db_helper)
        return chng_log.run(self)
