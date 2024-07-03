import time

import falcon
from jinja2 import Template
from uro_app.model import Project, Assembly, Package, Vulnerability, Changelog


def replace_empty_value(value_dict):
    for elem in value_dict:
        for el in elem.keys():
            if elem[el] == '' or elem[el] is None or elem[el] == 'None':
                elem[el] = '-'
    return value_dict


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        delta = (te - ts) * 1000
        print(f'{method.__name__} выполнялся {delta:2.2f} ms')
        return result

    return timed


def timeit_all_methods(cls):
    class NewCls:
        def __init__(self, *args, **kwargs):
            self._obj = cls(*args, **kwargs)

        def __getattribute__(self, s):
            try:
                x = super().__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            attr = self._obj.__getattribute__(s)
            if isinstance(attr, type(self.__init__)):
                return timeit(attr)
            else:
                return attr

    return NewCls


@timeit_all_methods
class ProjectResource:
    def __init__(self):
        self.prj = Project()

    def on_get(self, req, resp):
        self.prj = Project()
        resp.text = self.prj.get_prj()
        projects = resp.text
        proj = []
        for prj in projects:
            projects[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                projects[prj]['ss'] = 'even'
            projects[prj]['prj_id'] = prj
            proj.append(projects[prj])
        proj = replace_empty_value(proj)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/index.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'projects': proj})

    def on_post(self, req, resp):
        if 'AddSubmit' in req.media:
            raise falcon.HTTPMovedPermanently("/projects/add")
        if 'DeleteSubmit' in req.media:
            if req.media['DeleteSubmit'].isdigit():
                prj_id = int(req.media['DeleteSubmit'])
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/delete")
        if 'ViewAssm' in req.media:
            if req.media['ViewAssm'].isdigit():
                print(1)
                prj_id = int(req.media['ViewAssm'])
                prj_name = ''
                resp.text = self.prj.get_prj()
                projects = resp.text
                proj = []
                print(req.media)
                for prj in projects:
                    projects[prj]['ss'] = 'odd'
                    if int(prj) % 2 == 0:
                        projects[prj]['ss'] = 'even'
                    projects[prj]['prj_id'] = prj
                    proj.append(projects[prj])
                for i in proj:
                    if i['prj_id'] == int(req.media['ViewAssm']):
                        prj_name = i['prj_name']
                resp.text = '{"prj_name":' + f"'{prj_name}'" + '}'
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")
        else:
            raise falcon.HTTPMovedPermanently("/projects")


@timeit_all_methods
class ProjectDeleteResource:
    def on_get(self, req, resp, prj_id):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/delete_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp, prj_id):
        print(req.media)
        if 'confirm' in req.media:
            prj = Project()
            prj.delete = prj_id
            a = prj.delete_prj()
            print(a)
            if not a:
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/delete")
            else:
                resp.text = prj.get_prj()
                projects = resp.text
                proj = []
                for prj in projects:
                    projects[prj]['ss'] = 'odd'
                    if int(prj) % 2 == 0:
                        projects[prj]['ss'] = 'even'
                    projects[prj]['prj_id'] = prj
                    proj.append(projects[prj])
                resp.status = falcon.HTTP_OK
                resp.content_type = 'text/html'
                fp = open("uro_app/template/index.html", "r")
                tempobj = Template(fp.read())
                resp.text = tempobj.render({'projects': proj})
                raise falcon.HTTPMovedPermanently("/projects")
        else:
            raise falcon.HTTPMovedPermanently("/projects")


@timeit_all_methods
class ChooseAddProjectResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/choose_add_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp):
        if 'path' in req.media:
            raise falcon.HTTPMovedPermanently(f"/projects/add/path")
        else:
            raise falcon.HTTPMovedPermanently("/projects/add/input")


@timeit_all_methods
class ProjectAddInputResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/add_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp):
        prj = Project()
        prj.input = True
        prj.prj_name = req.media['project']
        prj.rel_name = req.media['release']
        prj.prj_desc = req.media['description']
        prj.vendor = req.media['vendor']
        prj.arch_name = req.media['architecture']
        a = False
        if prj.prj_name != '':
            a = prj.add_prj_input()
        else:
            print(2)
            raise falcon.HTTPMovedPermanently("/projects/add")
        if not a:
            print(1)
            raise falcon.HTTPMovedPermanently("/projects/already_exist")
        else:
            raise falcon.HTTPMovedPermanently("/projects")


@timeit_all_methods
class ProjectExisttResource:
    def on_get(self, req, input_type, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/already_exist.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()


@timeit_all_methods
class ProjectWrongPathResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/wrong_path.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()


@timeit_all_methods
class ProjectAddPathResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/add_path_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp):
        prj = Project()
        prj.l = True
        prj.path = req.media['path']
        a = prj.add_prj_path()
        if not a:
            raise falcon.HTTPMovedPermanently("/projects/wrong_path")
        else:
            raise falcon.HTTPMovedPermanently("/projects")


# добавить возвращение, если нет инфы
@timeit_all_methods
class AssemblyResource(object):  # get

    def on_get(self, req, resp, prj_id):
        pkg = Package()
        assm = Assembly()
        pkg.check_delete()
        resp.text = assm.get_assm(prj_id)
        assembly = []
        if resp.text is None:
            resp.text = {}
        else:
            projects = resp.text
            assembly = []
            for assm in projects:
                projects[assm]['ss'] = 'odd'
                if int(assm) % 2 == 0:
                    projects[assm]['ss'] = 'even'
                projects[assm]['assm_id'] = assm
                assembly.append(projects[assm])
        assembly = replace_empty_value(assembly)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/assembly.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'projects': assembly})

    def on_post(self, req, resp, prj_id):
        print(req.media)
        if 'AddSubmit' in req.media:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/add")
        if 'DeleteAssm' in req.media:
            if req.media['DeleteAssm'].isdigit():
                assm_id = int(req.media['DeleteAssm'])
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/delete")
        print(req.media)
        if 'ViewPkg' in req.media:
            if req.media['ViewPkg'].isdigit():
                assm_id = int(req.media['ViewPkg'])
                if "ViewJoint" in req.media:
                    raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/joint")
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package")
        if 'ViewVulnerability' in req.media:
            if req.media['ViewVulnerability'].isdigit():
                assm_id = int(req.media['ViewVulnerability'])
                if "ViewJoint" in req.media:
                    raise falcon.HTTPMovedPermanently(
                        f"/projects/{prj_id}/assembly/{assm_id}/joint/None/vulnerability/fixed")
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/vulnerability/fixed")
        if 'ViewResVulnerability' in req.media:
            if req.media['ViewResVulnerability'].isdigit():
                assm_id = int(req.media['ViewResVulnerability'])
                if "ViewJoint" in req.media:
                    raise falcon.HTTPMovedPermanently(
                        f"/projects/{prj_id}/assembly/{assm_id}/joint/None/vulnerability/resolved")
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/vulnerability/resolved")
        """if 'ViewJoint' in req.media:
            if req.media['ViewJoint'].isdigit():
                assm_id = int(req.media['ViewJoint'])
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/joint")"""
        if 'ViewCompare' in req.media:
            if req.media['ViewCompare'].isdigit():
                print(1)
                assm_id = int(req.media['ViewCompare'])
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/compare")
        print(req.media)
        raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")


@timeit_all_methods
class AddAssmResource:
    def on_get(self, req, resp, prj_id):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/add_path_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp, prj_id):
        assm = Assembly()
        assm.l = True
        assm.path = req.media['path']
        assm.deb = 'deb' in req.media
        assm.deb = 'pkg' in req.media
        assm.project = prj_id
        a = assm.add_assm()
        if not a:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/add")
        else:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")


@timeit_all_methods
class DeleteAssmResource:
    def on_get(self, req, resp, prj_id, assm_id):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/delete_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp, prj_id, assm_id):
        if 'confirm' in req.media:
            assm = Assembly()
            assm.delete = assm_id
            a = assm.delete_assm()
            if not a:
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/delete")
            else:
                resp.text = assm.get_assm(prj_id)
                projects = resp.text
                proj = []
                for prj in projects:
                    projects[prj]['ss'] = 'odd'
                    if int(prj) % 2 == 0:
                        projects[prj]['ss'] = 'even'
                    projects[prj]['assm_id'] = prj
                    proj.append(projects[prj])
                resp.status = falcon.HTTP_OK
                resp.content_type = 'text/html'
                fp = open("uro_app/template/assembly.html", "r")
                tempobj = Template(fp.read())
                resp.text = tempobj.render({'projects': proj})
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")
        else:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")


@timeit_all_methods
class AssemblyJointResource(object):
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id):
        self.pkg.assm_id = assm_id
        resp.text = self.pkg.get_joint_assm()
        packages = resp.text
        print(packages)
        proj = []
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            print(packages[prj]['joint_vers'])
            packages[prj]['date_created'] = packages[prj]['assm_date']
            packages[prj]['version'] = packages[prj]['joint_vers']
            packages[prj]['prj_id'] = prj_id
            packages[prj]['assm_id'] = assm_id
            proj.append(packages[prj])
        proj = replace_empty_value(proj)
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})

    def on_post(self, req, resp, prj_id, assm_id):
        if 'ViewVulnerability' in req.media:
            print(req.media['ViewVulnerability'])
            if req.media['ViewVulnerability'].isdigit():
                pkg_vul_id = req.media['ViewVulnerability']
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/"
                                                  f"joint/{pkg_vul_id}/vulnerability/fixed")
            else:
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/"
                                                  f"joint/{None}/vulnerability/fixed")
        if 'ViewResVulnerability' in req.media:
            if req.media['ViewResVulnerability'].isdigit():
                pkg_vul_id = req.media['ViewResVulnerability']
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/"
                                                  f"package/{pkg_vul_id}/vulnerability/resolved")
            else:
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/"
                                                  f"joint/{None}/vulnerability/resolved")
        if 'ViewChangelog' in req.media:
            if req.media['ViewChangelog'].isdigit():
                pkg_id = req.media['ViewChangelog']
                raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/changelog")
        else:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")


@timeit_all_methods
class AssemblyCompareResource(object):
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id):
        self.pkg.assm_id = assm_id
        resp.text = self.pkg.get_compare_assm()
        print(1)
        packages = resp.text
        proj = []
        print(packages)
        for pkg in packages:
            for key in packages[pkg].keys():
                if packages[pkg][key] is None:
                    packages[pkg][key] = ''
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            proj.append(packages[prj])
        proj += [{"prj_id": prj_id}]
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/compare_package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})

    def on_post(self, req, resp, prj_id, assm_id):
        print(req.media)
        self.pkg.dif_filter = [x for x in req.media if x in ('повышен', 'понижен', 'неизменен', 'удален', 'добавлен')]
        self.pkg.prev = 'prev' in req.media
        self.pkg.current = 'current' in req.media
        self.pkg.assm_id = assm_id
        resp.text = self.pkg.get_compare_assm()
        packages = resp.text
        proj = []
        for pkg in packages:
            for key in packages[pkg].keys():
                if packages[pkg][key] is None:
                    packages[pkg][key] = ''
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            proj.append(packages[prj])
        proj += [{"prj_id": prj_id, "assm_id": assm_id}]
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/compare_package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})


@timeit_all_methods
class PackageResource(object):  # get
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id):
        resp.text = self.pkg.get_pkg(assm_id)
        print(resp.text)
        packages = resp.text
        proj = []
        for pkg in packages:
            for key in packages[pkg].keys():
                if packages[pkg][key] is None:
                    packages[pkg][key] = ''
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            packages[prj]['date_created'] = packages[prj]['assm_date_created']
            proj.append(packages[prj])
        print(packages)
        proj = replace_empty_value(proj)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})

    def on_post(self, req, resp, prj_id, assm_id):
        if 'ViewChangelog' in req.media:
            pkg_id = req.media['ViewChangelog']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/changelog")
        if 'ViewVulnerability' in req.media:
            pkg_id = req.media['ViewVulnerability']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package"
                                              f"/{pkg_id}/vulnerability/resolved")
        if 'ViewResVulnerability' in req.media:
            pkg_id = req.media['ViewResVulnerability']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package"
                                              f"/{pkg_id}/vulnerability/fixed")
        else:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package")


@timeit_all_methods
class AssemblyCveResource(object):
    def __init__(self):
        self.cve = Vulnerability()

    def on_get(self, req, resp, prj_id, assm_id, resolved):
        self.cve = Vulnerability()
        self.cve.assm_id = assm_id
        self.cve.resolved = resolved == 'resolved'
        packages = self.cve.get_assm_cve()
        print(resp.text)
        vulnerability = []
        if len(packages) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': 0}]
        else:
            for prj in packages:
                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = prj
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = 0
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})

    def on_post(self, req, resp, prj_id, assm_id, resolved):
        self.cve = Vulnerability()
        self.cve.assm_id = assm_id
        self.cve.resolved = resolved == 'resolved'
        packages = self.cve.get_assm_cve(req.media)
        print(resp.text)
        vulnerability = []
        if len(packages) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': 0}]
        else:
            for prj in packages:
                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = prj
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = 0
                vulnerability.append(packages[prj])
        print(packages)
        vulnerability = replace_empty_value(vulnerability)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})


@timeit_all_methods
class PackageCveResource(object):
    def __init__(self):
        self.cve = Vulnerability()

    def on_get(self, req, resp, prj_id, assm_id, pkg_id, resolved):
        self.cve = Vulnerability()
        self.cve.pkg_vrs_id = pkg_id
        self.cve.resolved = resolved == 'resolved'
        resp.text = self.cve.get_pkg_cve()
        packages = resp.text
        vulnerability = []
        i = 0
        if len(packages) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': pkg_id}]
        else:
            for prj in packages:

                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = i

                req.context.role = f'{i}'
                req.context.user = 'guest'
                i += 1
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = pkg_id
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        print(vulnerability)
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})

    def on_post(self, req, resp, prj_id, assm_id, pkg_id, resolved):
        self.cve = Vulnerability()
        print(req.media)
        self.cve.pkg_vrs_id = pkg_id
        self.cve.resolved = resolved == 'resolved'
        resp.text = self.cve.get_pkg_cve(req.media)
        packages = resp.text
        vulnerability = []
        if len(packages) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': pkg_id}]

        else:
            i = 0
            for prj in packages:

                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = i

                req.context.role = f'{i}'
                req.context.user = 'guest'
                i += 1
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = pkg_id
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        resp.status = falcon.HTTP_OK

        # resp.content_type = falcon.MEDIA_JSON

        resp.content_type = 'text/html'
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})


@timeit_all_methods
class JointCveResource(object):

    def on_get(self, req, resp, prj_id, assm_id, pkg_vul_id, resolved):
        self.cve = Vulnerability()
        self.cve.pkg_vul_id = pkg_vul_id
        self.cve.assm_id = assm_id
        self.cve.resolved = resolved == 'resolved'
        resp.text = self.cve.get_joint_assm_cve()
        packages = resp.text
        vulnerability = []
        if len(resp.text) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': 0}]
        else:
            for prj in packages:
                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = prj
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = 0
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        if len(vulnerability) == 0:
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")
        resp.status = falcon.HTTP_OK
        # resp.content_type = falcon.MEDIA_JSON

        resp.content_type = 'text/html'
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})

    def on_post(self, req, resp, prj_id, assm_id, pkg_vul_id, resolved):
        self.cve = Vulnerability()
        self.cve.pkg_vul_id = pkg_vul_id
        self.cve.assm_id = assm_id
        self.cve.resolved = resolved == 'resolved'
        resp.text = self.cve.get_joint_assm_cve(req.media)
        packages = resp.text
        vulnerability = []
        if len(resp.text) == 0:
            vulnerability = [{'pkg_name': None,
                              'pkg_vers': None, 'deb_vers': None,
                              'cve_name': None,
                              'cve_desc': None, 'st_name': None, 'urg_name': None, 'rep_name': None,
                              'link': None, 'vul_ident': None, 'vul_name': None, 'vul_desc': None,
                              'date_discovered': None, 'cvss2_vector': None, 'cvss2_score': None,
                              'cvss3_vector': None, 'cvss3_score': None, 'severity': None, 'cwe_name': None,
                              'url': None, 'ss': 'odd', 'cve_id': None, 'prj_id': prj_id, 'assm_id': assm_id,
                              'pkg_id': 0}]
        else:
            for prj in packages:
                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['cve_id'] = prj
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = 0
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        resp.status = falcon.HTTP_OK
        # resp.content_type = falcon.MEDIA_JSON

        resp.content_type = 'text/html'
        fp = open("uro_app/template/vulnerability.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'vulnerability': vulnerability})


@timeit_all_methods
class ChangelogResource(object):
    def __init__(self):
        self.chng = Changelog()

    def on_get(self, req, resp, prj_id, assm_id, pkg_id):
        self.chng.pkg_id = pkg_id
        resp.text = self.chng.get_chng()
        print(resp.text)
        resp.status = falcon.HTTP_OK
        packages = resp.text
        print(pkg_id)
        vulnerability = []
        if len(packages) == 0:
            vulnerability = [{'log_desc': None, 'urg_name': None, 'date_added': None, 'log_ident': None, 'rep_name': None,
                         'ss': 'odd', 'prj_id': prj_id, 'assm_id': assm_id, 'pkg_id': pkg_id}]
        else:
            for prj in packages:
                packages[prj]['ss'] = 'odd'
                if int(prj) % 2 == 0:
                    packages[prj]['ss'] = 'even'
                packages[prj]['prj_id'] = prj_id
                packages[prj]['assm_id'] = assm_id
                packages[prj]['pkg_id'] = pkg_id
                vulnerability.append(packages[prj])
        vulnerability = replace_empty_value(vulnerability)
        print(vulnerability)
        #        if len(vulnerability) == 0:
        #           raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package")
        resp.content_type = 'text/html'
        fp = open("uro_app/template/changelog.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'chngs': vulnerability})
