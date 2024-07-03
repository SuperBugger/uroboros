CREATE SCHEMA temp_bdu;
CREATE TABLE temp_bdu.cwe (cwe_id serial4 NOT NULL, cwe_name text UNIQUE NOT NULL,
CONSTRAINT cwe_pkey PRIMARY KEY (cwe_id)
);
CREATE TABLE temp_bdu.identifier (
ident_id serial4 NOT NULL,
ident_type text NULL,
link text NULL,
ident_name text UNIQUE NOT NULL,
CONSTRAINT identifiers_pkey PRIMARY KEY (ident_id)
);
CREATE TABLE temp_bdu.vulnerability (
vul_id serial4 NOT NULL,
vul_ident text UNIQUE NOT NULL,
vul_name text NULL,
vul_desc text NULL,
date_discovered timestamptz NULL,
cvss2_vector text NULL,
cvss2_score text NULL,
cvss3_vector text NULL,
cvss3_score text NULL,
severity text NULL,
CONSTRAINT fstek_element_pkey PRIMARY KEY (vul_id)
);
CREATE TABLE temp_bdu.vul_cwe (
	vul_id int4 NOT NULL,
	cwe_id int4 NOT NULL,
	CONSTRAINT vul_cwe_pkey PRIMARY KEY (vul_id, cwe_id)
);
CREATE TABLE temp_bdu.vul_ident (
vul_id serial4 NOT NULL,
ident_id int4 NOT NULL,
CONSTRAINT vul_ident_pkey PRIMARY KEY (vul_id, ident_id)
);
CREATE TABLE temp_bdu.vul_sources (
vul_src_id serial4 NOT NULL,
url text NULL,
vul_id int4 NULL,
CONSTRAINT vul_sources_pkey PRIMARY KEY (vul_src_id)
);
