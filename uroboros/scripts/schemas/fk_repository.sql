ALTER TABLE temp_repository.assembly add CONSTRAINT assembly_prj_id_fkey
FOREIGN KEY (prj_id) REFERENCES temp_repository.project(prj_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.assm_pkg_vrs add CONSTRAINT assm_pkg_vrs_pkg_vrs_id_fkey
FOREIGN KEY (pkg_vrs_id) REFERENCES temp_repository.pkg_version(pkg_vrs_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.assm_pkg_vrs add CONSTRAINT assm_pkg_vrs_assm_id_fkey
FOREIGN KEY (assm_id) REFERENCES temp_repository.assembly(assm_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.changelog add CONSTRAINT changelog_urg_id_fkey
FOREIGN KEY (urg_id) REFERENCES temp_repository.urgency(urg_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.changelog add CONSTRAINT changelog_pkg_vrs_id_fkey
FOREIGN KEY (pkg_vrs_id) REFERENCES temp_repository.pkg_version(pkg_vrs_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.pkg_version add CONSTRAINT pkg_version_pkg_id_fkey
FOREIGN KEY (pkg_id) REFERENCES temp_repository.package(pkg_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.project add CONSTRAINT project_rep_id_fkey
FOREIGN KEY (rel_id) REFERENCES temp_repository.release(rel_id)
ON DELETE CASCADE;

ALTER TABLE temp_repository.project add CONSTRAINT project_arch_id_fkey
FOREIGN KEY (arch_id) REFERENCES temp_repository.architecture(arch_id)
ON DELETE CASCADE;

