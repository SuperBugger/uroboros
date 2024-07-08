"""

python3 -m uroboros.cli.update debtracker -f <path>
python3 -m uroboros.cli.update bdu -u --noclean
python3 -m uroboros.cli.update debtracker

"""

from uroboros.cli.updater_commands.jsonupdater import JsonUpdater
from datetime import datetime


class TrackerUpdater(JsonUpdater):
    def __init__(self, db_helper):
        super().__init__()
        self._db_helper = db_helper
        self._url = 'https://security-tracker.debian.org/tracker/data/json'

    def update_debtracker(self):
        print("Tracker_updater_process")
        try:
            up_pkg = self._ensure_uptable("package", ["pkg_id", "pkg_name"])
            up_cve = self._ensure_uptable("cve", ["cve_id", "cve_name", "cve_desc"])
            up_rel = self._ensure_uptable("release", ["rel_id", "rel_name"])
            up_st = self._ensure_uptable("status", ["st_id", "st_name"])
            up_urg = self._ensure_uptable("urgency", ["urg_id", "urg_name"])
            up_pkg_vrs = self._ensure_uptable("pkg_version", ["pkg_vrs_id", "version", "pkg_id"])
            up_rep = self._ensure_uptable("repository", ["rep_id", "rep_name", "rel_id"])
            up_cve_rep = self._ensure_uptable("cve_rep", ["cve_id", "rep_id", "pkg_resolved_id",
                                                          "urg_id", "st_id", "fixed_pkg_vrs_id"])
            packages = self._dict_tracker.keys()
            for package in packages:  # package - имя пакета
                up_pkg._schm = "temp_debtracker"
                pkg_id = up_pkg.getid(package)
                up_pkg.upsert(pkg_id, [pkg_id, package])
                cves = self._dict_tracker[package]
                for cve in cves.keys():  # cve имя cve
                    up_cve._schm = "temp_debtracker"
                    cve_id = up_cve.getid(cve)
                    elms = cves[cve]
                    desc = None
                    if "description" in elms:
                        desc = elms["description"]
                    up_cve.upsert(cve_id, [cve_id, cve, desc])
                    rls = elms["releases"]
                    for rl in rls.keys():  # релизы
                        up_rel._schm = "temp_debtracker"
                        rel_id = up_rel.getid(rl)
                        up_rel.upsert(rel_id, [rel_id, rl])
                        elem_rel = rls[rl]
                        up_st._schm = "temp_debtracker"
                        st_id = up_st.getid(elem_rel["status"])
                        up_st.upsert(st_id, [st_id, elem_rel["status"]])
                        fixed_pkg_vrs_id = None
                        pkg_resolved_id = None
                        up_urg._schm = "temp_debtracker"
                        urg_id = up_urg.getid(elem_rel["urgency"])
                        up_urg.upsert(urg_id, [urg_id, elem_rel["urgency"]])
                        if "fixed_version" in elem_rel:  # проверка
                            up_pkg_vrs._schm = "temp_debtracker"
                            fixed_pkg_vrs_id = up_pkg_vrs.getid((elem_rel["fixed_version"], pkg_id))
                            up_pkg_vrs.upsert(fixed_pkg_vrs_id, [fixed_pkg_vrs_id, elem_rel["fixed_version"], pkg_id])
                        reps = elem_rel["repositories"]
                        for rep in reps.keys():
                            up_rep._schm = "temp_debtracker"
                            rep_id = up_rep.getid(rep)
                            up_rep.upsert(rep_id, [rep_id, rep, rel_id])
                            up_pkg_vrs._schm = "temp_debtracker"
                            if fixed_pkg_vrs_id is None:
                                fixed_pkg_vrs_id = up_pkg_vrs.getid((reps[rep], pkg_id))
                                up_pkg_vrs.upsert(fixed_pkg_vrs_id, [fixed_pkg_vrs_id, reps[rep], pkg_id])
                            else:
                                pkg_resolved_id = up_pkg_vrs.getid((reps[rep], pkg_id))
                                up_pkg_vrs.upsert(pkg_resolved_id, [pkg_resolved_id, reps[rep], pkg_id])
                            up_cve_rep._schm = "temp_debtracker"
                            up_cve_rep.upsert((cve_id, rep_id), [cve_id, rep_id, pkg_resolved_id,
                                                                 urg_id, st_id, fixed_pkg_vrs_id])

        except KeyError as ex:
            print(ex)
            self._error("parsing json.")

    def run(self, no_clean, file, l):
        print(datetime.now(), "Start")
        if l:
            self._download_obj(self._url)
            self._get_data('data/json')
        if file:
            self._get_data(file)
        self._create_temp_schema("debtracker")
        self.update_debtracker()
        self._upload_tables()
        self._merge_schemas()
        self._db_helper.commit_conn()
        self._add_fk()
        self.replace_schema(no_clean)
        if not no_clean:
            # self._delete_old_schema()
            self._clear_trash()
        print(datetime.now(), "Successful")
        print("End time", datetime.now() - self.start_time)

