"""
python3 -m uroboros.cli.manage prj --input
python3 -m uroboros.cli.manage prj -l --path <path>

python3 -m uroboros.cli.manage prj --delete --project <prj_id>

"""
import os
import re
from cli.manage_commands.base_uploader import time_decorator
from cli.manage_commands.data_uploader import DataUploader

from api.manage_commands.project_uploader import ProjectUploaderApi


class ProjectUploader(DataUploader):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper
        self.up_prj = self._ensure_uptable("project", ["prj_id", "prj_name", "rel_id",
                                                       "prj_desc", "vendor", "arch_id"], "prj_id",
                                           ['rel_id', 'arch_id'])
        self.rls_tbl = self._ensure_uptable("release", ["rel_id", "rel_name"], "rel_id", [])
        self.arch_tbl = self._ensure_uptable("architecture", ["arch_id", "arch_name"], "arch_id", [])
        self.up_prj._schm = "repositories"
        self.rls_tbl._schm = "repositories"
        self.arch_tbl._schm = "repositories"

    @time_decorator
    def delete_project(self, prj_id):
        try:
            assm_del = []
            pkg_del = []
            pkg_vrs_del = []
            result_sql = f"DELETE FROM repositories.project WHERE prj_id = {prj_id};"
            sql = f"SELECT assm_id from repositories.assembly where prj_id={prj_id}"
            for assm_id in self._db_helper.query(sql):
                assm_del.append(assm_id[0])
                result_sql += f"DELETE FROM repositories.assembly WHERE assm_id = {assm_id[0]};"
            self._db_helper.query(result_sql)
            self._db_helper.commit_conn()
            for assm_id in assm_del:
                sql = f"select pkg_vrs_id, pkg_id from repositories.pkg_version " \
                      f"where pkg_vrs_id not in (SELECT pkg_vrs_id " \
                      f"from repositories.assm_pkg_vrs where assm_id={assm_id})"
                for pkg_list in self._db_helper.query(sql):
                    sql = f"select count(*) from repositories.assm_pkg_vrs rapv" \
                          f" join repositories.pkg_version rpv on rpv.pkg_vrs_id = rapv.pkg_vrs_id" \
                          f" join repositories.package rp on rpv.pkg_id=rp.pkg_id and rp.pkg_id={pkg_list[1]} "
                    if self._db_helper.query(sql)[0][0] < 1:
                        pkg_del.append(pkg_list[1])
                        pkg_vrs_del.append(pkg_list[0])
            result_sql = ""
            for p_id in pkg_vrs_del:
                result_sql += f"DELETE FROM repositories.pkg_version WHERE pkg_vrs_id = {p_id};"
            for p_id in pkg_del:
                result_sql += f"DELETE FROM repositories.package WHERE pkg_id = {p_id};"
            if len(result_sql) != 0:
                self._db_helper.query(result_sql)
                self._db_helper.commit_conn()
                result_sql = ""
            sql = f"select arch_id from repositories.architecture " \
                  f"where arch_id not in (select arch_id from repositories.project)"
            if len(self._db_helper.query(sql)) != 0:
                arch_list = self._db_helper.query(sql)
                for arch_id in arch_list:
                    result_sql += f"DELETE FROM repositories.architecture WHERE arch_id = {arch_id[0]};"
            sql = f"select rel_id from repositories.release " \
                  f"where rel_id not in (select rel_id from repositories.project)"
            if len(self._db_helper.query(sql)) != 0:
                rel_list = self._db_helper.query(sql)
                if rel_list[0] is not None:
                    for arch_id in rel_list:
                        result_sql += f"DELETE FROM repositories.release WHERE rel_id = {arch_id[0]};"
            sql = f"select urg_id from repositories.urgency " \
                  f"where urg_id not in (select urg_id from repositories.changelog)"
            if len(self._db_helper.query(sql)) != 0:
                urg_list = self._db_helper.query(sql)
                if urg_list[0] is not None:
                    for arch_id in urg_list:
                        result_sql += f"DELETE FROM repositories.urgency WHERE urg_id = {arch_id[0]};"
            if len(result_sql) != 0:
                self._db_helper.query(result_sql)
                self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("Deleting project")

    @time_decorator
    def check_project(self, prj_name=None, prj_id=None, rel_name=None, arch_name=None, delete=False):
        try:
            sql = f"SELECT EXISTS(SELECT prj_name " \
                  f"from repositories.project rp"
            if isinstance(rel_name, str) and isinstance(arch_name, str):
                if not re.search(r"\w", prj_name):
                    print("Wrong project name")
                    exit(1)
                if re.search(r'\w', rel_name):
                    sql = f"SELECT EXISTS(SELECT prj_id, prj_name, rr.rel_name " \
                          f"from repositories.project rp"
                    sql += f" join repositories.release rr on rr.rel_id=rp.rel_id and rr.rel_name='{rel_name}'"
                if re.search(r'\w', arch_name):
                    sql = f"SELECT EXISTS(SELECT prj_id, prj_name, ra.arch_name " \
                          f"from repositories.project rp"
                    sql += f" join repositories.architecture ra " \
                           f"on rp.arch_id = ra.arch_id and ra.arch_name='{arch_name}'"
                if re.search(r'\w', rel_name) and re.search(r'\w', arch_name):
                    sql = f"SELECT EXISTS(SELECT prj_id, prj_name, rr.rel_name, ra.arch_name " \
                          f"from repositories.project rp"
                    sql += f" join repositories.release rr on rr.rel_id=rp.rel_id and rr.rel_name='{rel_name}'"
                    sql += f" join repositories.architecture ra " \
                           f"on rp.arch_id = ra.arch_id and ra.arch_name='{arch_name}'"
            if prj_id is None:
                sql += f" where prj_name='{prj_name}');"
            else:
                sql += f" where prj_id={prj_id});"
            if self._db_helper.query(sql)[0][0] and not delete:
                print("The project already exists")
                exit(1)
            if not self._db_helper.query(sql)[0][0] and delete:
                print("The project doesn't exist")
                exit(1)
        except Exception as e:
            print(e)
            self._error("processing project")

    @time_decorator
    def processing_project_name(self, name):
        try:
            prj_id = self.up_prj.getid(name, sql_attr="prj_name")
            self.up_prj.upsert(prj_id, [prj_id, name, None, None, None, None])
            return self.up_prj
        except Exception as e:
            print(e)
            self._error("processing source repository. Project")

    @time_decorator
    def processing_project_input(self):
        try:
            rel_id = None
            arch_id = None
            prj_name = input("Input project name: ")
            rel_name = input("Input project repository: ")
            arch_name = input("Input architecture: ")
            prj_desc = input("Input project description: ")
            vendor = input("Input vendor of project: ")
            self.check_project(prj_name=prj_name, rel_name=rel_name, arch_name=arch_name)
            if re.search(r'\w', rel_name):
                rel_id = self.rls_tbl.getid(rel_name, sql_attr="rel_name")
                self.rls_tbl.upsert(rel_id, [rel_id, rel_name])
            if re.search(r'\w', arch_name):
                arch_id = self.arch_tbl.getid(arch_name, sql_attr="arch_name")
                self.arch_tbl.upsert(arch_id, [arch_id, arch_name])
            if re.search(r'\w', prj_name):
                prj_id = self.up_prj.getid(prj_name)
                self.up_prj.upsert(prj_id, [prj_id, prj_name, rel_id, prj_desc, vendor, arch_id])
        except Exception as e:
            print(e)
            self._error("processing project input")

    @time_decorator
    def run(self, args):
        assm = ProjectUploaderApi(self._db_helper)
        assm.run(args)