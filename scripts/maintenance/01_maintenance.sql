CREATE SCHEMA maintenance;
CREATE TABLE maintenance.schema_vrs (
schm_name text NOT NULL,
schm_vrs text NOT NULL,
schm_user text NOT NULL,
schm_url text NULL,
date_changed timestamptz NOT NULL,
CONSTRAINT schema_vrs_pkey PRIMARY KEY (schm_name)
);

CREATE TABLE maintenance.update_info (
ui_date timestamptz NOT NULL DEFAULT now(),
ui_user text NULL DEFAULT CURRENT_USER,
ui_records int4 NULL,
ui_name text NULL,
CONSTRAINT update_info_pkey PRIMARY KEY (ui_date)
);

CREATE OR REPLACE PROCEDURE maintenance.update_debtracker()
 LANGUAGE plpgsql
AS $procedure$
declare 
max_id INTEGER;
  begin

	 select max(st_id) into max_id from temp_debtracker.status;
	SELECT setval('temp_debtracker.status_st_id_seq', max_id, true) into max_id;

	 select max(urg_id) into max_id from temp_debtracker.urgency;
	SELECT setval('temp_debtracker.urgency_urg_id_seq', max_id, true) into max_id;

	 select max(cve_id) into max_id from temp_debtracker.cve;
	SELECT setval('temp_debtracker.cve_cve_id_seq', max_id, true) into max_id;

	 select max(pkg_id) into max_id from temp_debtracker.package;
	SELECT setval('temp_debtracker.package_pkg_id_seq', max_id, true) into max_id;

	 select max(rel_id) into max_id from temp_debtracker."release";
	SELECT setval('temp_debtracker.release_rel_id_seq', max_id, true) into max_id;

	 select max(rep_id) into max_id from temp_debtracker.repository;
	SELECT setval('temp_debtracker.repository_rep_id_seq', max_id, true) into max_id;

	 select max(pkg_vrs_id) into max_id from temp_debtracker.pkg_version;
	SELECT setval('temp_debtracker.pkg_version_pkg_vrs_id_seq', max_id, true) into max_id;

	insert into temp_debtracker.status
	(st_name)
	select st_name
	from debtracker.status
	on conflict (st_name) do nothing;

	insert into temp_debtracker.urgency
	(urg_name)
	select urg_name
	from debtracker.urgency
	on conflict (urg_name) do nothing;

	insert into temp_debtracker.cve
	(cve_name, cve_desc)
	select cve_name, cve_desc
	from debtracker.cve
	on conflict (cve_name) do nothing;

	insert into temp_debtracker."release"
	(rel_name)
	select rel_name
	from debtracker."release"
	on conflict (rel_name) do nothing;

	insert into temp_debtracker.repository
	(rep_name, rel_id)
	select dr.rep_name, tr.rel_id
	from debtracker.repository dr
   	join debtracker."release" drr on drr.rel_id = dr.rel_id
   	join temp_debtracker."release" tr using(rel_name)
   	on conflict (rep_name) do nothing;
	
 	insert into temp_debtracker.package
 	(pkg_name)
 	select pkg_name
 	from debtracker.package
 	on conflict (pkg_name) do nothing;
 
 	insert into temp_debtracker.pkg_version
 	("version", pkg_id)
	SELECT "version", pkg_id FROM (
  	SELECT dpv."version", tp.pkg_id 
  	FROM debtracker.pkg_version dpv
  	join debtracker.package dp on dp.pkg_id = dpv.pkg_id  
  	join temp_debtracker.package tp using(pkg_name)
	) as pkg
	WHERE ("version", pkg_id) not in (select "version", pkg_id 
					from temp_debtracker.pkg_version);
								
		insert into temp_debtracker.cve_rep
    (cve_id, rep_id, pkg_resolved_id, urg_id, st_id, fixed_pkg_vrs_id)
	select
  	tdc.cve_id,
  	tdr.rep_id,
  	(select pkg_vrs_id from temp_debtracker.pkg_version tdpv where tdpv.pkg_id = tdp.pkg_id and tdpv."version" = dpv."version") as resolved,
  	(select urg_id from temp_debtracker.urgency tdu where tdu.urg_name = du.urg_name) as urg_id,
  	(select st_id from temp_debtracker.status tds where tds.st_name = ds.st_name) as st_id,
  	(select pkg_vrs_id from temp_debtracker.pkg_version tdpvv where tdpvv.pkg_id = tdp.pkg_id and tdpvv."version" = dpvv."version") as fixed
	from debtracker.cve_rep dcr
	join debtracker.cve dc on dcr.cve_id = dc.cve_id
	join debtracker.repository dr on dcr.rep_id = dr.rep_id
	join debtracker.urgency du on dcr.urg_id = du.urg_id
	join debtracker.status ds on dcr.st_id = ds.st_id
	join debtracker.pkg_version dpv on dcr.pkg_resolved_id = dpv.pkg_vrs_id
	join debtracker.package  dp on dp.pkg_id = dpv.pkg_id
	join debtracker.pkg_version dpvv on dcr.fixed_pkg_vrs_id = dpvv.pkg_vrs_id
	join temp_debtracker.cve tdc on tdc.cve_name = dc.cve_name
	join temp_debtracker.repository tdr on tdr.rep_name = dr.rep_name
	join temp_debtracker.package tdp on tdp.pkg_name = dp.pkg_name 
	left join temp_debtracker.cve_rep tdcr on tdcr.rep_id = tdr.rep_id and tdcr.cve_id = tdc.cve_id
	where tdcr.rep_id is null;
 end;
$procedure$
;

CREATE OR REPLACE PROCEDURE maintenance.update_bdu()
 LANGUAGE plpgsql
AS $procedure$
declare
v_id INTEGER;
max_id INTEGER;
c_id INTEGER;
i_id integer;
vul RECORD;
cwe_name RECORD;
ident RECORD;
  begin
	  	select max(tc.cwe_id) into max_id from temp_bdu.cwe tc;
		SELECT setval('temp_bdu.cwe_cwe_id_seq', max_id, true) into max_id;

	 	select max(ti.ident_id) into max_id from temp_bdu.identifier ti;
		SELECT setval('temp_bdu.identifier_ident_id_seq', max_id, true) into max_id;

	 select max(tv.vul_id) into max_id from temp_bdu.vulnerability tv;
	SELECT setval('temp_bdu.vulnerability_vul_id_seq', max_id, true) into max_id;

	 select max(tvs.vul_src_id) into max_id from temp_bdu.vul_sources tvs;
	SELECT setval('temp_bdu.vul_sources_vul_src_id_seq', max_id, true) into max_id;

	  	insert into temp_bdu.cwe (cwe_name)
   		select c.cwe_name
   		from bdu.cwe c
   		where c.cwe_name not in(
   				select tc.cwe_name 
   				from temp_bdu.cwe tc);

   		insert into temp_bdu.identifier
   		(ident_type, link, ident_name)
    	select i.ident_type, i.link, i.ident_name
    	from bdu.identifier i
    	where i.ident_name not in(
    			select ti.ident_name 
    			from temp_bdu.identifier ti);

	  for vul in (select *
	  				from bdu.vulnerability
	  				where vul_ident not in (
	  				select vul_ident
	  				from temp_bdu.vul_ident))
	  	loop
			if vul.vul_ident not in (
			select vul_ident
	  		from temp_bdu.vul_ident) then
	  		
				insert into temp_bdu.vulnerability
	  			(vul_ident, vul_name, vul_desc,
    			date_discovered, severity, cvss2_vector,
    			cvss2_score, cvss3_vector, cvss3_score)
    			values (vul.vul_ident, vul.vul_name, vul.vul_desc,
    			vul.date_discovered, vul.severity, vul.cvss2_vector,
    			vul.cvss2_score, vul.cvss3_vector, vul.cvss3_score)
    			returning vul_id INTO v_id;
    		
	  		end if;
	  	
			insert into temp_bdu.vul_sources (url, vul_id)
    		select bvs.url, v_id
   			from bdu.vul_sources bvs
   			join vul v on v.vul_id = bvs.vul_id
			on conflict (vul_id) do nothing;
	
  			for cwe_name in (select cwe_name
  							from bdu.cwe
  							where cwe_id in (
  							select cwe_id 
  							from bdu.vul_cwe vc
  							where vul_id  = vul.vul_id))
  			loop
	  				select cwe_id into c_id 
	  				from temp_bdu.cwe 
	  				where cwe_name = cwe_name; 
	  				
  					insert into temp_bdu.vul_cwe
  					(vul_id, cwe_id)
  					values
  					(v_id, c_id)
  					on conflict(vul_id, cwe_id) do nothing;
  			end loop;

  			for ident in (select ident_name
  							 from bdu.identifier 
  							 where ident_id in (
  							 select ident_id 
  							 from bdu.vul_ident 
  							 where vul_id = vul.vul_id))
  			loop	
	  				select ident_id into i_id
	  				from temp_bdu.identifier
	  				where ident_name = ident.ident_name;
	  				
  					insert into temp_bdu.vul_ident
  					(vul_id, ident_id)
  					values
  					(v_id, i_id)
  					on conflict (vul_id, ident_id) do nothing;
  			end loop;

  		end loop;

  END;
 $procedure$
;

CREATE OR REPLACE PROCEDURE maintenance.update_rep_pkg()
 LANGUAGE plpgsql
AS $procedure$
	declare
max_id INTEGER;
	begin
	select max(arch_id) into max_id from repositories.architecture;
	SELECT setval('repositories.architecture_arch_id_seq', max_id, true) into max_id;

		select max(assm_id) into max_id from repositories.assembly;
	SELECT setval('repositories.assembly_assm_id_seq', max_id, true) into max_id;

select max(id) into max_id from repositories.changelog;
	SELECT setval('repositories.changelog_id_seq', max_id, true) into max_id;

		select max(rel_id) into max_id from repositories."release";
	SELECT setval('repositories.release_rel_id_seq', max_id, true) into max_id;

select max(prj_id) into max_id from repositories.project;
	SELECT setval('repositories.project_prj_id_seq', max_id, true) into max_id;

		select max(urg_id) into max_id from repositories.urgency;
	SELECT setval('repositories.urgency_urg_id_seq', max_id, true) into max_id;

	select max(pkg_vrs_id) into max_id from repositories.pkg_version;
	SELECT setval('repositories.pkg_version_pkg_vrs_id_seq', max_id, true) into max_id;

		select max(pkg_id) into max_id from repositories.package;
	SELECT setval('repositories.package_pkg_id_seq', max_id, true) into max_id;

	END;
$procedure$
;

-- DROP FUNCTION maintenance.get_assm_cve(bool, int4);

CREATE OR REPLACE FUNCTION maintenance.get_assm_cve(resolved boolean, asm_id integer)
 RETURNS TABLE(pkg_name text, asm_version text, pkg_version text, cve_name text, cve_desc text, st_name text, urg_name text, rep_name text, link text, vul_ident text, vul_name text, vul_desc text, date_discovered timestamp with time zone, cvss2_vector text, cvss2_score text, cvss3_vector text, cvss3_score text, severity text, cwe_name text, url text)
 LANGUAGE plpgsql
 ROWS 10000
AS $function$
	begin
		if resolved = false then
		return query (select pkg_assm.pkg_name, dpv."version", pkg_assm."version", dc.cve_name, dc.cve_desc,
         ds.st_name, du.urg_name, dr.rep_name, bi.link, bv.vul_ident, bv.vul_name, bv.vul_desc, bv.date_discovered, bv.cvss2_vector,
		bv.cvss2_score, bv.cvss3_vector, bv.cvss3_score, bv.severity, bc.cwe_name, bvs.url from
		(select rp.pkg_name, pv2."version" from repositories.assembly a
		join repositories.assm_pkg_vrs apv on apv.assm_id = a.assm_id
		join repositories.pkg_version pv2 on pv2.pkg_vrs_id = apv.pkg_vrs_id
		join repositories.package rp on rp.pkg_id=pv2.pkg_id
		where a.assm_id = asm_id
		) as pkg_assm
		join debtracker.package dp on pkg_assm.pkg_name = dp.pkg_name
		join debtracker.pkg_version dpv on dp.pkg_id=dpv.pkg_id
		join debtracker.cve_rep dcr on dpv.pkg_vrs_id = dcr.fixed_pkg_vrs_id
		join debtracker.cve dc on dc.cve_id = dcr.cve_id
		join debtracker.repository dr on dr.rep_id=dcr.rep_id
		join debtracker.urgency du on du.urg_id=dcr.urg_id
		join debtracker.status ds on ds.st_id=dcr.st_id
		left join bdu.identifier bi on bi.ident_name = dc.cve_name
		left join bdu.vul_ident bvi on bvi.ident_id = bi.ident_id
		left join bdu.vulnerability bv on bv.vul_id = bvi.vul_id
		left join bdu.vul_sources bvs on bvs.vul_id = bv.vul_id
		left join bdu.vul_cwe bvc on bvc.vul_id = bv.vul_id
		left join bdu.cwe bc on bc.cwe_id = bvc.cwe_id
		where pkg_assm."version">=dpv."version");
		end if;

		if resolved = true then
		return query (select pkg_assm.pkg_name, dpv."version", pkg_assm."version", dc.cve_name, dc.cve_desc,
         ds.st_name, du.urg_name, dr.rep_name,  bi.link, bv.vul_ident, bv.vul_name, bv.vul_desc, bv.date_discovered, bv.cvss2_vector,
		bv.cvss2_score, bv.cvss3_vector, bv.cvss3_score, bv.severity, bc.cwe_name, bvs.url from
		(select rp.pkg_name, pv2."version" from repositories.assembly a
		join repositories.assm_pkg_vrs apv on apv.assm_id = a.assm_id
		join repositories.pkg_version pv2 on pv2.pkg_vrs_id = apv.pkg_vrs_id
		join repositories.package rp on rp.pkg_id=pv2.pkg_id
		where a.assm_id = asm_id
		) as pkg_assm
		join debtracker.package dp on pkg_assm.pkg_name = dp.pkg_name
		join debtracker.pkg_version dpv on dp.pkg_id=dpv.pkg_id
		join debtracker.cve_rep dcr on dpv.pkg_vrs_id = dcr.pkg_resolved_id
		join debtracker.cve dc on dc.cve_id = dcr.cve_id
		join debtracker.repository dr on dr.rep_id=dcr.rep_id
		join debtracker.urgency du on du.urg_id=dcr.urg_id
		join debtracker.status ds on ds.st_id=dcr.st_id
		left join bdu.identifier bi on bi.ident_name = dc.cve_name
		left join bdu.vul_ident bvi on bvi.ident_id = bi.ident_id
		left join bdu.vulnerability bv on bv.vul_id = bvi.vul_id
		left join bdu.vul_sources bvs on bvs.vul_id = bv.vul_id
		left join bdu.vul_cwe bvc on bvc.vul_id = bv.vul_id
		left join bdu.cwe bc on bc.cwe_id = bvc.cwe_id
		where pkg_assm."version">=dpv."version" and ds.st_name <> 'open');
	end if;
	END;
$function$
;


-- DROP FUNCTION maintenance.get_pkg_cve(bool, int4);

CREATE OR REPLACE FUNCTION maintenance.get_pkg_cve(resolved boolean, p_id integer)
 RETURNS TABLE(pkg_name text, asm_version text, pkg_version text, cve_name text, cve_desc text, st_name text, urg_name text, rep_name text, link text, vul_ident text, vul_name text, vul_desc text, date_discovered timestamp with time zone, cvss2_vector text, cvss2_score text, cvss3_vector text, cvss3_score text, severity text, cwe_name text, url text)
 LANGUAGE plpgsql
 ROWS 10000
AS $function$
	begin
		if resolved = false then
		return query (select rp.pkg_name, rpv."version", dpv."version", dc.cve_name, dc.cve_desc,
         ds.st_name, du.urg_name, dr.rep_name, bi.link, bv.vul_ident, bv.vul_name, bv.vul_desc, bv.date_discovered, bv.cvss2_vector,
		bv.cvss2_score, bv.cvss3_vector, bv.cvss3_score, bv.severity, bc.cwe_name, bvs.url
        from repositories.pkg_version rpv
        join repositories.package rp on rpv.pkg_id = rp.pkg_id
        join debtracker.package dp using(pkg_name)
		join debtracker.pkg_version dpv on dp.pkg_id=dpv.pkg_id
		join debtracker.cve_rep dcr on dpv.pkg_vrs_id = dcr.fixed_pkg_vrs_id
		join debtracker.cve dc on dc.cve_id = dcr.cve_id
		join debtracker.repository dr on dr.rep_id=dcr.rep_id
		join debtracker.urgency du on du.urg_id=dcr.urg_id
		join debtracker.status ds on ds.st_id=dcr.st_id
		left join bdu.identifier bi on bi.ident_name = dc.cve_name
		left join bdu.vul_ident bvi on bvi.ident_id = bi.ident_id
		left join bdu.vulnerability bv on bv.vul_id = bvi.vul_id
		left join bdu.vul_sources bvs on bvs.vul_id = bv.vul_id
		left join bdu.vul_cwe bvc on bvc.vul_id = bv.vul_id
		left join bdu.cwe bc on bc.cwe_id = bvc.cwe_id
		where rpv.pkg_vrs_id = p_id and rpv."version">=dpv."version");
		end if;
		if resolved = true then
		return query (select rp.pkg_name, rpv."version", dpv."version", dc.cve_name, dc.cve_desc,
         ds.st_name, du.urg_name, dr.rep_name, bi.link, bv.vul_ident, bv.vul_name, bv.vul_desc, bv.date_discovered, bv.cvss2_vector,
		bv.cvss2_score, bv.cvss3_vector, bv.cvss3_score, bv.severity, bc.cwe_name, bvs.url
        from repositories.pkg_version rpv
        join repositories.package rp on rpv.pkg_id = rp.pkg_id
        join debtracker.package dp using(pkg_name)
		join debtracker.pkg_version dpv on dp.pkg_id=dpv.pkg_id
		join debtracker.cve_rep dcr on dpv.pkg_vrs_id = dcr.pkg_resolved_id
		join debtracker.cve dc on dc.cve_id = dcr.cve_id
		join debtracker.repository dr on dr.rep_id=dcr.rep_id
		join debtracker.urgency du on du.urg_id=dcr.urg_id
		join debtracker.status ds on ds.st_id=dcr.st_id
		left join bdu.identifier bi on bi.ident_name = dc.cve_name
		left join bdu.vul_ident bvi on bvi.ident_id = bi.ident_id
		left join bdu.vulnerability bv on bv.vul_id = bvi.vul_id
		left join bdu.vul_sources bvs on bvs.vul_id = bv.vul_id
		left join bdu.vul_cwe bvc on bvc.vul_id = bv.vul_id
		left join bdu.cwe bc on bc.cwe_id = bvc.cwe_id
		where rpv.pkg_vrs_id = p_id and rpv."version">=dpv."version" and ds.st_name<>'open');
	end if;
	END;
$function$
;



-- DROP PROCEDURE maintenance.compare_assm(int4);

CREATE OR REPLACE PROCEDURE maintenance.compare_assm(IN a_id integer)
 LANGUAGE plpgsql
AS $procedure$
declare
date_created timestamptz;
proj_id integer;
start_date timestamptz;
	begin

		select prj_id into proj_id
		from repositories.assembly a
		where assm_id = a_id;

		select assm_date_created into date_created
		from repositories.assembly a
		where assm_id = a_id;

		insert into maintenance.compare_assm
		(pkg_name, curr_vers, curr_date, vers_status,
		assm_date, pkg_vers, prev, current_assm)
		select CASE
		when l.now_pkg is NULL
			THEN l.old_pkg
			ELSE l.now_pkg
		end as pkg_name,
		l.vers, l.assm, l.st as text, l.date_prev, l.max_prev, false, true
		from (
			select aa.pkg_name as old_pkg, s.pkg_name as now_pkg, aa.vers, aa.assm,
			CASE
				WHEN aa.vers>s.max_prev THEN 'повышен'
			    WHEN aa.vers<s.max_prev THEN 'понижен'
				WHEN aa.vers=s.max_prev THEN 'неизменен'
				WHEN aa.vers is NULL THEN 'удален'
				ELSE 'добавлен'
		    end as st,
		    s.date_prev, s.max_prev
		    from (
				select p.pkg_name, max(pv."version") as vers, max(a.assm_date_created) as assm
				from repositories.pkg_version pv
				join repositories.assm_pkg_vrs apv on apv.pkg_vrs_id = pv.pkg_vrs_id
				join repositories.assembly a on a.assm_id = apv.assm_id
				join repositories.package p on p.pkg_id = pv.pkg_id
				where assm_date_created  = date_created
				group by p.pkg_name) as aa
			full join (
				select e.pkg_name, max(e.assm_date_created) as date_prev, max(e."version") as max_prev
				from (
					select rp.pkg_name, a2.assm_date_created, pv3."version"
					from repositories.package rp
					join repositories.pkg_version pv3 on pv3.pkg_id = rp.pkg_id
					join repositories.assm_pkg_vrs apv2 on apv2.pkg_vrs_id = pv3.pkg_vrs_id
					join repositories.assembly a2 on a2.assm_id = apv2.assm_id
					where a2.assm_date_created < date_created and prj_id=proj_id) as e
					group by e.pkg_name
						) as s on s.pkg_name = aa.pkg_name
					) as l
			order by pkg_name;

		select assm_date_created into start_date
		from repositories.assembly
		where assm_date_created < date_created::timestamptz
		and prj_id = proj_id
		order by assm_date_created desc
		limit 1;

		insert into maintenance.compare_assm
		(pkg_name, curr_vers, curr_date, vers_status,
		assm_date, pkg_vers, prev, current_assm)
		select CASE
				when l.now_pkg is NULL
					THEN l.old_pkg
					ELSE l.now_pkg
		       		end as pkg_name,
		l.vers, l.assm, l.st as text, l.date_prev, l.max_prev, true, false
		from (
			select aa.pkg_name as old_pkg, s.pkg_name as now_pkg, aa.vers, aa.assm,
			CASE
				WHEN aa.vers>s.max_prev THEN 'повышен'
			    WHEN aa.vers<s.max_prev THEN 'понижен'
	            WHEN aa.vers=s.max_prev THEN 'неизменен'
	            WHEN aa.vers is NULL THEN 'удален' 
	            ELSE 'добавлен'
		   	end as st,
		    s.date_prev, s.max_prev from (
				select p.pkg_name, max(pv."version") as vers, max(a.assm_date_created) as assm
				from repositories.pkg_version pv
				join repositories.assm_pkg_vrs apv on apv.pkg_vrs_id = pv.pkg_vrs_id
				join repositories.assembly a on a.assm_id = apv.assm_id
				join repositories.package p on p.pkg_id = pv.pkg_id
				where assm_date_created  = start_date
				group by p.pkg_name) as aa
			full join (
				select e.pkg_name, max(e.assm_date_created) as date_prev, max(e."version") as max_prev from
					(select rp.pkg_name, a2.assm_date_created, pv3."version"
					from repositories.package rp
					join repositories.pkg_version pv3 on pv3.pkg_id = rp.pkg_id
					join repositories.assm_pkg_vrs apv2 on apv2.pkg_vrs_id = pv3.pkg_vrs_id
					join repositories.assembly a2 on a2.assm_id = apv2.assm_id
					where a2.assm_date_created < start_date and prj_id=proj_id) as e
					group by e.pkg_name
					) as s on s.pkg_name = aa.pkg_name
				) as l
			order by pkg_name;


		select assm_date_created into start_date
		from repositories.assembly
		where assm_date_created < date_created::timestamptz
		and prj_id = proj_id
		order by assm_date_created desc
		limit 1;

		insert into maintenance.compare_assm
		(pkg_name, curr_vers, curr_date, vers_status, assm_date, pkg_vers, prev, current_assm)
		select CASE
			when l.now_pkg is NULL THEN l.old_pkg
			ELSE l.now_pkg
		end as pkg_name,
		l.vers, l.assm, l.st as text, l.date_prev, l.max_prev, true, true
		from (
			select aa.pkg_name as old_pkg, s.pkg_name as now_pkg, aa.vers, aa.assm,
			CASE
				WHEN aa.vers>s.max_prev THEN 'повышен'
		   		WHEN aa.vers<s.max_prev THEN 'понижен'
		        WHEN aa.vers=s.max_prev THEN 'неизменен'
	            WHEN aa.vers is NULL THEN 'удален'
		        ELSE 'добавлен'
		   	end as st,
		    s.date_prev, s.max_prev  from (
				select p.pkg_name, max(pv."version") as vers, max(a.assm_date_created) as assm
				from repositories.pkg_version pv
				join repositories.assm_pkg_vrs apv on apv.pkg_vrs_id = pv.pkg_vrs_id
				join repositories.assembly a on a.assm_id = apv.assm_id
				join repositories.package p on p.pkg_id = pv.pkg_id
				where assm_date_created  = date_created
				group by p.pkg_name) as aa
			full join (
				select e.pkg_name, max(e.assm_date_created) as date_prev, max(e."version") as max_prev from
					(select rp.pkg_name, a2.assm_date_created, pv3."version"
					from repositories.package rp
					join repositories.pkg_version pv3 on pv3.pkg_id = rp.pkg_id
					join repositories.assm_pkg_vrs apv2 on apv2.pkg_vrs_id = pv3.pkg_vrs_id
					join repositories.assembly a2 on a2.assm_id = apv2.assm_id
					where a2.assm_date_created = start_date and prj_id=proj_id) as e
					group by e.pkg_name
					) as s on s.pkg_name = aa.pkg_name
				) as l
			order by pkg_name;
		
		select assm_date_created into start_date
		from repositories.assembly
		where assm_date_created < date_created::timestamptz
		and prj_id = proj_id
		order by assm_date_created desc
		limit 1;


	END;


$procedure$
;



-- DROP PROCEDURE maintenance.get_joint_assm(int4);

CREATE OR REPLACE PROCEDURE maintenance.get_joint_assm(IN a_id integer)
 LANGUAGE plpgsql
AS $procedure$
declare
date_created timestamptz;
proj_id integer;
	begin

		select prj_id into proj_id
		from repositories.assembly a
		where assm_id = a_id;
	

		select assm_date_created into date_created
		from repositories.assembly a
		where assm_id = a_id;

		insert into maintenance.assm_vul
		(pkg_vul_id, pkg_name,  joint_vers, cve_vers, cve_name, cve_desc,
         st_name, urg_name, rep_name, link,
         vul_ident, vul_name, vul_desc, date_discovered,
         cvss2_vector, cvss2_score, cvss3_vector, cvss3_score,
         severity, cwe_name, url)
		select dense_rank() over (order by join_assm.pkg_name) as s, 
 join_assm.pkg_name, join_assm.vers,  pv."version",
		dc.cve_name, dc.cve_desc, ds.st_name, du.urg_name,dr.rep_name, bi.link, bv.vul_ident, bv.vul_name, bv.vul_desc, bv.date_discovered, bv.cvss2_vector,
		bv.cvss2_score, bv.cvss3_vector, bv.cvss3_score, bv.severity, bc.cwe_name, bvs.url
		from
		(
			select p.pkg_name, max(pv."version") as vers, max(a.assm_date_created) as max_date
			from repositories.pkg_version pv, repositories.pkg_version pv2
			join repositories.assm_pkg_vrs apv on apv.pkg_vrs_id = pv2.pkg_vrs_id
			join repositories.assembly a on a.assm_id = apv.assm_id
			join repositories.package p on p.pkg_id = pv2.pkg_id
			where assm_date_created <= date_created and prj_id = proj_id and pv.pkg_id=pv2.pkg_id
			group by p.pkg_name
		) as join_assm
		left join debtracker.package dp on join_assm.pkg_name = dp.pkg_name
		left join debtracker.pkg_version pv on dp.pkg_id =  pv.pkg_id and pv."version" < join_assm.vers
		left join debtracker.cve_rep dcr on dcr.fixed_pkg_vrs_id = pv.pkg_vrs_id or dcr.pkg_resolved_id = pv.pkg_vrs_id
		left join debtracker.repository dr on dr.rep_id = dcr.rep_id
		left join debtracker.urgency du on du.urg_id = dcr.urg_id
		left join debtracker.status ds on ds.st_id = dcr.st_id
		left join debtracker.cve dc on dc.cve_id = dcr.cve_id
		left join bdu.identifier bi on bi.ident_name = dc.cve_name
		left join bdu.vul_ident bvi on bvi.ident_id = bi.ident_id
		left join bdu.vulnerability bv on bv.vul_id = bvi.vul_id
		left join bdu.vul_sources bvs on bvs.vul_id = bv.vul_id
		left join bdu.vul_cwe bvc on bvc.vul_id = bv.vul_id
		left join bdu.cwe bc on bc.cwe_id = bvc.cwe_id;
		--where pv."version" < join_assm.vers;

	END;
$procedure$
;


