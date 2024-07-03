CREATE SCHEMA bdu;
CREATE TABLE bdu.cwe (cwe_id serial4 NOT NULL, cwe_name text UNIQUE NOT NULL, CONSTRAINT cwe_pkey PRIMARY KEY (cwe_id));
CREATE TABLE bdu.identifier (
ident_id serial4 NOT NULL,
ident_type text NULL,
link text NULL,
ident_name text UNIQUE NULL,
CONSTRAINT identifiers_pkey PRIMARY KEY (ident_id)
);
CREATE TABLE bdu.vulnerability (
vul_id serial4 NOT NULL,
vul_ident text UNIQUE NULL,
vul_name text NULL,
vul_desc text NULL,
date_discovered timestamptz NULL,
severity text NULL,
cvss2_vector text NULL,
cvss2_score text NULL,
cvss3_vector text NULL,
cvss3_score text NULL,
CONSTRAINT fstek_element_pkey PRIMARY KEY (vul_id)
);
CREATE TABLE bdu.vul_cwe (
	vul_id int4 NOT NULL,
	cwe_id int4 NOT NULL,
	CONSTRAINT vul_cwe_pkey PRIMARY KEY (vul_id, cwe_id),
	CONSTRAINT vul_cwe_cwe_id_fkey FOREIGN KEY (cwe_id) REFERENCES bdu.cwe(cwe_id) ON DELETE CASCADE,
	CONSTRAINT vul_cwe_vul_id_fkey FOREIGN KEY (vul_id) REFERENCES bdu.vulnerability(vul_id) ON DELETE CASCADE
);
CREATE TABLE bdu.vul_ident (
vul_id serial4 NOT NULL,
ident_id int4 NOT NULL,
CONSTRAINT vul_ident_pkey PRIMARY KEY (vul_id, ident_id),
CONSTRAINT vul_ident_ident_id_fkey FOREIGN KEY (ident_id) REFERENCES bdu.identifier(ident_id) ON DELETE CASCADE,
CONSTRAINT vul_ident_vul_id_fkey FOREIGN KEY (vul_id) REFERENCES bdu.vulnerability(vul_id) ON DELETE CASCADE
);
CREATE TABLE bdu.vul_sources (
vul_src_id serial4 NOT NULL,
url text NULL,
vul_id int4 NULL,
CONSTRAINT vul_sources_pkey PRIMARY KEY (vul_src_id),
CONSTRAINT vul_sources_vul_id_fkey FOREIGN KEY (vul_id) REFERENCES bdu.vulnerability(vul_id) ON DELETE CASCADE
);
