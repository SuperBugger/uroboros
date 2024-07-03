CREATE SCHEMA debtracker;
CREATE TABLE debtracker.cve (
cve_id serial4 NOT NULL,
cve_name text UNIQUE NOT NULL,
cve_desc text NULL,
CONSTRAINT cve_pkey PRIMARY KEY (cve_id)
);
CREATE TABLE debtracker.package (
pkg_id serial4 NOT NULL,
pkg_name text UNIQUE NULL,
CONSTRAINT source_package_pkey PRIMARY KEY (pkg_id)
);
CREATE TABLE debtracker.pkg_version (
pkg_vrs_id serial4 NOT NULL,
"version" text NULL,
pkg_id int4 NULL,
CONSTRAINT version_package_pkey PRIMARY KEY (pkg_vrs_id),
CONSTRAINT version_package_pkg_id_fkey FOREIGN KEY (pkg_id) REFERENCES debtracker.package(pkg_id) ON DELETE CASCADE
);
CREATE TABLE debtracker."release" (
rel_id serial4 NOT NULL,
rel_name text UNIQUE NOT NULL,
CONSTRAINT release_pkey PRIMARY KEY (rel_id)
);
CREATE TABLE debtracker.repository (
rep_id serial4 NOT NULL,
rep_name text UNIQUE NOT NULL,
rel_id int4 NULL,
CONSTRAINT repository_pkey PRIMARY KEY (rep_id),
CONSTRAINT repository_rel_id_fkey FOREIGN KEY (rel_id) REFERENCES debtracker."release"(rel_id) ON DELETE CASCADE
);
CREATE TABLE debtracker.status (
st_id serial4 NOT NULL,
st_name text NULL,
CONSTRAINT status_pkey PRIMARY KEY (st_id)
);
CREATE TABLE debtracker.urgency (
urg_id serial4 NOT NULL,
urg_name text NULL,
CONSTRAINT urgency_pkey PRIMARY KEY (urg_id)
);
CREATE TABLE debtracker.cve_rep (
cve_id int4 NOT NULL,
rep_id int4 NOT NULL,
pkg_resolved_id int4 NULL,
urg_id int4 NULL,
st_id int4 NULL,
fixed_pkg_vrs_id int4 NULL,
CONSTRAINT cve_rep_pkey PRIMARY KEY (cve_id, rep_id),
CONSTRAINT cve_rep_cve_id_fkey FOREIGN KEY (cve_id) REFERENCES debtracker.cve(cve_id) ON DELETE CASCADE,
CONSTRAINT cve_rep_pkg_vul_id_fkey FOREIGN KEY (fixed_pkg_vrs_id) REFERENCES debtracker.pkg_version(pkg_vrs_id) ON DELETE CASCADE,
CONSTRAINT cve_rep_rep_id_fkey FOREIGN KEY (rep_id) REFERENCES debtracker.repository(rep_id) ON DELETE CASCADE,
CONSTRAINT cve_rep_st_id_fkey FOREIGN KEY (st_id) REFERENCES debtracker.status(st_id) ON DELETE CASCADE,
CONSTRAINT cve_rep_urg_id_fkey FOREIGN KEY (urg_id) REFERENCES debtracker.urgency(urg_id) ON DELETE CASCADE,
CONSTRAINT cve_rep_vrs_pkg_id_fkey FOREIGN KEY (pkg_resolved_id) REFERENCES debtracker.pkg_version(pkg_vrs_id) ON DELETE CASCADE
);

CREATE INDEX  ON debtracker.pkg_version ("version", pkg_id);