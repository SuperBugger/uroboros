import json
import os

import falcon
# import jinja2
from jinja2 import Template
from uro_app.model import Project, Assembly, Package, Vulnerability, Changelog


class ProjectResource:  # get
    def __init__(self):
        self.prj = Project()

    def on_get(self, req, resp):
        projects = self.prj.get_prj()
        proj = []
        for prj in projects:
            projects[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                projects[prj]['ss'] = 'even'
            projects[prj]['prj_id'] = prj
            proj.append(projects[prj])
        print(projects)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        fp = open("uro_app/template/index.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'projects': proj})

    def on_post(self, req, resp):
        if 'AddSubmit' in req.media:
            raise falcon.HTTPMovedPermanently("/projects/add")
        if 'DeleteSubmit' in req.media:
            prj_id = req.media.prj_id
            self.prj.delete_prj(prj_id)
        if 'ViewAssm' in req.media:
            prj_id = req.media['prj_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly")
        resp.text = self.prj.get_prj()
        projects = json.loads(resp.text)
        proj = []
        for prj in projects:
            projects[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                projects[prj]['ss'] = 'even'
            projects[prj]['prj_id'] = prj
            proj.append(projects[prj])
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        fp = open("uro_app/template/index.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'projects': proj})

    """def on_put_student(self, req, resp, id):
        pass

    def on_delete_student(self, req, resp, id):
        pass"""


class ProjectDeleteResource:
    pass


class ProjectAddResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        fp = open("uro_app/template/add_project.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render()

    def on_post(self, req, resp):
        print(req.media)
        raise falcon.HTTPMovedPermanently("/projects/add")


class AssemblyResource(object):  # get
    def __init__(self):
        self.assm = Assembly()

    def on_get(self, req, resp, prj_id):
        assm = self.assm.get_assm(prj_id)
        proj = []
        for prj in assm:
            assm[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                assm[prj]['ss'] = 'even'
            assm[prj]['assm_id'] = prj
            proj.append(assm[prj])
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/assembly.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'projects': proj})

    def on_post(self, req, resp, prj_id):
        if 'AddSubmit' in req.media:
            raise falcon.HTTPMovedPermanently("/projects/add")
        if 'DeleteAssm' in req.media:
            assm_id = req.media['assm_id']
        if 'ViewPkg' in req.media:
            assm_id = req.media['assm_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package")
        if 'ViewVulnerability' in req.media:
            assm_id = req.media['assm_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/vulnerability/fixed")
        if 'ViewResVulnerability' in req.media:
            assm_id = req.media['assm_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/vulnerability/resolved")
        if 'ViewCompare' in req.media:
            assm_id = req.media['assm_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/compare/no_prev/is_current")


class AddAssmResource:
    pass


class DeleteAssmResource:
    pass


class AssemblyJointResource(object):
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id):
        self.pkg.assm_id = assm_id
        self.pkg.joint = True
        packages = self.pkg.get_pkg()
        proj = []
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            proj.append(packages[prj])
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})


class AssemblyCompareResource(object):
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id, prev, current):
        print(11111111111)
        self.pkg.assm_id = assm_id
        self.pkg.difference = True
        if prev == 'is_prev':
            self.pkg.prev = True
        else:
            self.pkg.prev = False
        if current == 'is_current':
            self.pkg.current = True
        else:
            self.pkg.current = False
        print(11111111111)
        packages = self.pkg.get_pkg()
        proj = []
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            proj.append(packages[prj])
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        #fp = open("uro_app/template/package.html", "r")
        #tempobj = Template(fp.read())
        #resp.text = tempobj.render({'packages': proj})

    def on_post(self):
        pass


class PackageResource(object):  # get
    def __init__(self):
        self.pkg = Package()

    def on_get(self, req, resp, prj_id, assm_id):
        self.pkg.assm_id = assm_id
        packages = self.pkg.get_pkg()
        proj = []
        for prj in packages:
            packages[prj]['ss'] = 'odd'
            if int(prj) % 2 == 0:
                packages[prj]['ss'] = 'even'
            packages[prj]['pkg_vrs_id'] = prj
            proj.append(packages[prj])
        print(packages)
        resp.status = falcon.HTTP_OK
        resp.content_type = 'text/html'
        fp = open("uro_app/template/package.html", "r")
        tempobj = Template(fp.read())
        resp.text = tempobj.render({'packages': proj})

    def on_post(self, req, resp, prj_id, assm_id):
        if 'ViewChangelog' in req.media:
            pkg_id = req.media['pkg_vrs_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/changelog")
        if 'ViewVulnerability' in req.media:
            pkg_id = req.media['pkg_vrs_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package"
                                              f"/{pkg_id}/vulnerability/fixed")
        if 'ViewResVulnerability' in req.media:
            pkg_id = req.media['pkg_vrs_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/package"
                                              f"/{pkg_id}/vulnerability/resolved")
        if 'ViewCompare' in req.media:
            assm_id = req.media['assm_id']
            raise falcon.HTTPMovedPermanently(f"/projects/{prj_id}/assembly/{assm_id}/compare")


class AssemblyCveResource(object):
    def __init__(self):
        self.cve = Vulnerability()

    def on_get(self, req, resp, prj_id, assm_id, resolved):
        self.cve.assm_id = assm_id
        if resolved == 'resolved':
            self.cve.resolved = True
        resp.text = json.dumps(self.cve.get_cve())
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON


class PackageCveResource(object):
    def __init__(self):
        self.cve = Vulnerability()

    def on_get(self, req, resp, prj_id, assm_id, pkg_id, resolved):
        self.cve.pkg_vrs_id = pkg_id
        if resolved == 'resolved':
            self.cve.resolved = True
        resp.text = self.cve.get_cve()
        print(resp.text)
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON


class JointCveResource(object):
    def __init__(self):
        self.cve = Vulnerability(joint=True)

    def on_get(self, req, resp, prj_id, assm_id, resolved):
        self.cve.assm_id = assm_id
        if resolved == 'resolved':
            self.cve.resolved = True
        resp.text = self.cve.get_cve()
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON


class ChangelogResource:
    def on_get(self, req, resp, prj_id, assm_id, pkg_id):
        self.chng = Changelog(pkg_id)
        resp.text = self.chng.get_chng()
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON
