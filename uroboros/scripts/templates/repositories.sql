CREATE SCHEMA temp_repositories;
CREATE TABLE temp_repositories.architecture (
arch_id serial4 NOT NULL,
arch_name text NULL
);
CREATE TABLE temp_repositories."release" (
rel_id serial4 NOT NULL,
rel_name text NULL
);

CREATE TABLE temp_repositories.project (
prj_id serial4 NOT NULL,
prj_name text NULL,
rel_id int4 NULL,
prj_desc text NULL,
vendor text NULL,
arch_id int4 NULL
);
CREATE TABLE temp_repositories.package (
pkg_id serial4 NOT NULL,
pkg_name text NULL
);
CREATE TABLE temp_repositories.pkg_version (
pkg_vrs_id serial4 NOT NULL,
author_name text NULL,
pkg_id int4 NULL,
"version" text NULL
);
CREATE TABLE temp_repositories.assembly (
assm_id serial4 NOT NULL,
assm_date_created timestamptz NULL,
assm_desc text NULL,
prj_id int4 NULL,
assm_version text NULL
);
CREATE TABLE temp_repositories.assm_pkg_vrs (
pkg_vrs_id int4 NOT NULL,
assm_id int4 NOT NULL
);
CREATE TABLE temp_repositories.urgency (
urg_id serial4 NOT NULL,
urg_name text NULL
);
CREATE TABLE temp_repositories.changelog (
id serial4 NOT NULL,
log_desc text NOT NULL,
urg_id int4 NOT NULL,
pkg_vrs_id int4 NULL,
date_added timestamptz NOT NULL,
log_ident text NULL,
rep_name text NULL
);
