CREATE SCHEMA temp_debtracker;
CREATE TABLE temp_debtracker.cve (
cve_id serial4 NOT NULL,
cve_name text UNIQUE NULL,
cve_desc text NULL,
CONSTRAINT cve_pkey PRIMARY KEY (cve_id)
);
CREATE TABLE temp_debtracker.package (
pkg_id serial4 NOT NULL,
pkg_name text UNIQUE NULL,
CONSTRAINT source_package_pkey PRIMARY KEY (pkg_id)
);
CREATE TABLE temp_debtracker.pkg_version (
pkg_vrs_id serial4 NOT NULL,
"version" text NULL,
pkg_id int4 NULL,
CONSTRAINT version_package_pkey PRIMARY KEY (pkg_vrs_id)
);
CREATE TABLE temp_debtracker."release" (
rel_id serial4 NOT NULL,
rel_name text UNIQUE NULL,
CONSTRAINT release_pkey PRIMARY KEY (rel_id)
);
CREATE TABLE temp_debtracker.repository (
rep_id serial4 NOT NULL,
rep_name text NULL,
rel_id int4 NULL,
CONSTRAINT repository_pkey PRIMARY KEY (rep_id)
);
CREATE TABLE temp_debtracker.status (
st_id serial4 NOT NULL,
st_name text UNIQUE NULL,
CONSTRAINT status_pkey PRIMARY KEY (st_id)
);
CREATE TABLE temp_debtracker.urgency (
urg_id serial4 NOT NULL,
urg_name text UNIQUE NULL,
CONSTRAINT urgency_pkey PRIMARY KEY (urg_id)
);
CREATE TABLE temp_debtracker.cve_rep (
cve_id int4 NOT NULL,
rep_id int4 NOT NULL,
pkg_resolved_id int4 NULL,
urg_id int4 NULL,
st_id int4 NULL,
fixed_pkg_vrs_id int4 NULL,
CONSTRAINT cve_rep_pkey PRIMARY KEY (cve_id, rep_id)
);

alter table temp_debtracker.pkg_version add constraint unique_pkg_version_version_pkg_id UNIQUE ("version", pkg_id);

alter table temp_debtracker.repository add constraint unique_rep_name UNIQUE (rep_name);
