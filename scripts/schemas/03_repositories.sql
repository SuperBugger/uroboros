CREATE SCHEMA repositories;
CREATE TABLE repositories.architecture (
arch_id serial4 NOT NULL,
arch_name text UNIQUE NOT NULL,
CONSTRAINT architecture_pkey PRIMARY KEY (arch_id)
);
CREATE TABLE repositories."release" (
rel_id serial4 NOT NULL,
rel_name text UNIQUE NOT NULL,
CONSTRAINT release_pkey PRIMARY KEY (rel_id)
);

CREATE TABLE repositories.project (
prj_id serial4 NOT NULL,
prj_name text NOT NULL,
rel_id int4 NULL,
prj_desc text NULL,
vendor text NULL,
arch_id int4 NULL,
CONSTRAINT project_pkey PRIMARY KEY (prj_id),
CONSTRAINT project_arch_id_fkey FOREIGN KEY (arch_id) REFERENCES repositories.architecture(arch_id),
CONSTRAINT project_rel_id_fkey FOREIGN KEY (rel_id) REFERENCES repositories.release(rel_id)
);
CREATE TABLE repositories.package (
pkg_id serial4 NOT NULL,
pkg_name text UNIQUE NOT NULL,
CONSTRAINT package_pkey PRIMARY KEY (pkg_id)
);
CREATE TABLE repositories.pkg_version (
pkg_vrs_id serial4 NOT NULL,
pkg_date_created timestamptz NULL,
author_name text NULL,
pkg_id int4 NULL,
"version" text NULL,
CONSTRAINT version_package_pkey PRIMARY KEY (pkg_vrs_id),
CONSTRAINT version_package_pkg_id_fkey FOREIGN KEY (pkg_id) REFERENCES repositories.package(pkg_id)
);
CREATE TABLE repositories.assembly (
assm_id serial4 NOT NULL,
assm_date_created timestamptz NULL,
assm_desc text NULL,
prj_id int4 NOT NULL,
assm_version text NOT NULL,
CONSTRAINT assembly_pkey PRIMARY KEY (assm_id),
CONSTRAINT assembly_prj_id_fkey FOREIGN KEY (prj_id) REFERENCES repositories.project(prj_id) ON DELETE CASCADE
);
CREATE TABLE repositories.assm_pkg_vrs (
pkg_vrs_id int4 NOT NULL,
assm_id int4 NOT NULL,
CONSTRAINT assm_pkg_vrs_pkey PRIMARY KEY (assm_id, pkg_vrs_id),
CONSTRAINT assm_pkg_vrs_assm_id_fkey FOREIGN KEY (assm_id) REFERENCES repositories.assembly(assm_id) ON DELETE CASCADE,
CONSTRAINT assm_pkg_vrs_pkg_vrs_id_fkey FOREIGN KEY (pkg_vrs_id) REFERENCES repositories.pkg_version(pkg_vrs_id) ON DELETE CASCADE
);
CREATE TABLE repositories.urgency (
urg_id serial4 NOT NULL,
urg_name text UNIQUE NOT NULL,
CONSTRAINT urgency_pkey PRIMARY KEY (urg_id)
);
CREATE TABLE repositories.changelog (
id serial4 NOT NULL,
log_desc text NOT NULL,
urg_id int4 NOT NULL,
pkg_vrs_id int4 NULL,
date_added timestamptz NOT NULL,
log_ident text NULL,
rep_name text NULL,
CONSTRAINT changelogs_pkey PRIMARY KEY (id),
CONSTRAINT changelog_urg_id_fkey FOREIGN KEY (urg_id) REFERENCES repositories.urgency(urg_id),
CONSTRAINT changelog_vrs_pkg_id_fkey FOREIGN KEY (pkg_vrs_id) REFERENCES repositories.pkg_version(pkg_vrs_id) ON DELETE CASCADE
);

alter table repositories.project add constraint unique_project_prj_name_rel_id_arch_id UNIQUE (prj_name, rel_id, arch_id);

alter table repositories.pkg_version add constraint unique_pkg_version_version_pkg_id UNIQUE ("version", pkg_id);

alter table repositories.assm_pkg_vrs add constraint unique_assm_pkg_vrs_assm_id_pkg_vrs_id UNIQUE (assm_id, pkg_vrs_id);