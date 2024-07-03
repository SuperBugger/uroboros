ALTER TABLE temp_bdu.vul_cwe add CONSTRAINT vul_cwe_cwe_id_fkey
FOREIGN KEY (cwe_id) REFERENCES temp_bdu.cwe(cwe_id)
ON DELETE CASCADE;

ALTER TABLE temp_bdu.vul_cwe add CONSTRAINT vul_cwe_vul_id_fkey
FOREIGN KEY (vul_id) REFERENCES temp_bdu.vulnerability(vul_id)
ON DELETE CASCADE;

ALTER TABLE temp_bdu.vul_ident add CONSTRAINT vul_ident_ident_id_fkey
FOREIGN KEY (ident_id) REFERENCES temp_bdu.identifier(ident_id)
ON DELETE CASCADE;

ALTER TABLE temp_bdu.vul_ident add CONSTRAINT vul_ident_vul_id_fkey
FOREIGN KEY (vul_id) REFERENCES temp_bdu.vulnerability(vul_id)
ON DELETE CASCADE;

ALTER TABLE temp_bdu.vul_sources add CONSTRAINT vul_src_vul_id_fkey
FOREIGN KEY (vul_id) REFERENCES temp_bdu.vulnerability(vul_id)
ON DELETE CASCADE;