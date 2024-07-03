ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_cve_id_fkey
FOREIGN KEY (cve_id) REFERENCES temp_debtracker.cve(cve_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_rep_id_fkey
FOREIGN KEY (rep_id) REFERENCES temp_debtracker.repository(rep_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_urg_id_fkey
FOREIGN KEY (urg_id) REFERENCES temp_debtracker.urgency(urg_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_st_id_fkey
FOREIGN KEY (st_id) REFERENCES temp_debtracker.status(st_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_pkg_resolved_id_fkey
FOREIGN KEY (pkg_resolved_id) REFERENCES temp_debtracker.pkg_version(pkg_vrs_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.cve_rep add CONSTRAINT cve_rep_fixed_pkg_vrs_id_fkey
FOREIGN KEY (fixed_pkg_vrs_id) REFERENCES temp_debtracker.pkg_version(pkg_vrs_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.repository add CONSTRAINT rep_rel_id_fkey
FOREIGN KEY (rel_id) REFERENCES temp_debtracker.release(rel_id)
ON DELETE CASCADE;

ALTER TABLE temp_debtracker.pkg_version add CONSTRAINT pkg_version_pkg_id_fkey
FOREIGN KEY (pkg_id) REFERENCES temp_debtracker.package(pkg_id)
ON DELETE CASCADE;