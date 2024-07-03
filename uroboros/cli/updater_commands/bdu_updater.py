"""
python3 -m uroboros.cli.update bdu -f <path>
python3 -m uroboros.cli.update bdu -u --noclean
python3 -m uroboros.cli.update bdu
"""

from cli.updater_commands.xmlupdater import XmlUpdater
from datetime import datetime


class BduUpdater(XmlUpdater):
    def __init__(self, helper):
        super().__init__()
        self._db_helper = helper
        self.up_vul = dict()
        self._url = 'https://bdu.fstec.ru/files/documents/vulxml.zip'

    def updater_bdu(self):
        print("Bdu_updater_process")
        up_bdu = self._ensure_uptable("vulnerability", ["vul_id", "vul_ident", "vul_name", "vul_desc",
                                                        "date_discovered", "cvss2_vector",
                                                        "cvss2_score", "cvss3_vector", "cvss3_score", "severity"
                                                        ])
        up_cwe = self._ensure_uptable("cwe", ["cwe_id", "cwe_name"])
        up_src = self._ensure_uptable("vul_sources", ["vul_src_id", "url", "vul_id"])
        up_identi = self._ensure_uptable("identifier", ["ident_id", "ident_type", "link",
                                                        "ident_name"])
        up_identi_vul = self._ensure_uptable("vul_ident", ["vul_id", "ident_id"])
        up_vul_cwe = self._ensure_uptable("vul_cwe", ["vul_id", "cwe_id"])
        up_bdu._schm = "temp_bdu"
        up_cwe._schm = "temp_bdu"
        up_src._schm = "temp_bdu"
        up_identi._schm = "temp_bdu"
        up_identi_vul._schm = "temp_bdu"
        up_vul_cwe._schm = "temp_bdu"
        try:
            for child in self._root:
                if child.tag == "vul":
                    bdu_row = {"vul_id": None, "vul_ident": None, "vul_name": None, "vul_desc": None,
                               "date_discovered": None, "cvss2_vector": None,
                               "cvss2_score": None, "cvss3_vector": None, "cvss3_score": None,
                               "severity": None
                               }
                    for vul_elem in child:
                        if vul_elem.tag == "identifier":
                            vul_id = up_bdu.getid(vul_elem.text)
                            bdu_row["vul_id"] = vul_id
                            bdu_row["vul_ident"] = vul_elem.text
                            continue
                        if vul_elem.tag == "name":
                            bdu_row["vul_name"] = vul_elem.text
                            continue
                        if vul_elem.tag == "description":
                            bdu_row["vul_desc"] = vul_elem.text
                            continue
                        if vul_elem.tag == "cwe":
                            for elem in vul_elem:
                                if elem.tag == "identifier":
                                    cwe_id = up_cwe.getid(elem.text)
                                    up_vul_cwe.upsert((bdu_row["vul_id"], cwe_id), [bdu_row["vul_id"], cwe_id])
                                    up_cwe.upsert(cwe_id, [cwe_id, elem.text])
                            continue
                        if vul_elem.tag == "identify_date":
                            bdu_row["date_discovered"] = vul_elem.text
                            continue
                        if vul_elem.tag == "cvss":
                            for elem in vul_elem:
                                bdu_row["cvss2_score"] = elem.attrib['score']
                                bdu_row["cvss2_vector"] = elem.text
                            continue
                        if vul_elem.tag == "cvss3":
                            for elem in vul_elem:
                                bdu_row["cvss3_score"] = elem.attrib['score']
                                bdu_row["cvss3_vector"] = elem.text
                            continue
                        if vul_elem.tag == "severity":
                            bdu_row["severity"] = vul_elem.text
                            continue
                        if vul_elem.tag == "sources":
                            if vul_elem.text is not None:
                                vul_src_id = up_src.getid(vul_elem.text)
                                up_src.upsert(vul_src_id, [vul_src_id, vul_elem.text, bdu_row["vul_id"]])
                        if vul_elem.tag == "identifiers":
                            for elem in vul_elem:
                                ident_id = up_identi.getid(elem.text)
                                link = None
                                if "link" in elem.attrib:
                                    link = elem.attrib['link']
                                up_identi.upsert(ident_id, [ident_id, elem.attrib['type'], link,
                                                            elem.text])
                                up_identi_vul.upsert((bdu_row["vul_id"], ident_id), [bdu_row["vul_id"], ident_id])
                            continue
                        if vul_elem.tag == "other":
                            up_bdu.upsert(bdu_row["vul_id"], [bdu_row["vul_id"], bdu_row["vul_ident"],
                                                              bdu_row["vul_name"], bdu_row["vul_desc"],
                                                              bdu_row["date_discovered"], bdu_row["cvss2_vector"],
                                                              bdu_row["cvss2_score"], bdu_row["cvss3_vector"],
                                                              bdu_row["cvss3_score"], bdu_row["severity"]])
                            continue
        except Exception as e:
            print(e)
            self._error(" parsing the xml tree")

    def run(self, no_clean, file, l):
        print(datetime.now(), "Start")
        if l:
            print(1)
            self._download_obj(self._url)
            self._get_data('data/vulxml.zip')
        else:
            self._get_data(file)
        self._create_temp_schema("bdu")
        self.updater_bdu()
        self._upload_tables()
        self._merge_schemas()
        self._db_helper.commit_conn()
        self._add_fk()
        self.replace_schema(no_clean)
        if not no_clean:
            # self._delete_temp_schema()
            self._clear_trash()
        print(datetime.now(), "Successful")
        print("time", datetime.now() - self.start_time)
