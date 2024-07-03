import pathlib

import falcon

from uro_app.resources import *
from uroboros.uro_app.resources import ChooseAddProjectResource, ProjectWrongPathResource, ProjectExisttResource, \
    ProjectAddPathResource, ProjectAddInputResource

app = falcon.App()

STATIC_PATH = pathlib.Path(__file__).parent / 'static'
print(STATIC_PATH)
app.add_static_route('/static', str(STATIC_PATH))
#app.add_route("/projects/{prj_id}", ProjectResource()) #+
app.add_route("/projects", ProjectResource()) #+
app.add_route("/projects/add", ChooseAddProjectResource()) #+
app.add_route("/projects/already_exist", ProjectExisttResource()) #+
app.add_route("/projects/wrong_path", ProjectWrongPathResource()) #+
app.add_route("/projects/add/path", ProjectAddPathResource()) #+
app.add_route("/projects/add/input", ProjectAddInputResource()) #+
app.add_route("/projects/{prj_id}/delete", ProjectDeleteResource()) #+
app.add_route('/projects/{prj_id}/assembly', AssemblyResource())  #+
app.add_route('/projects/{prj_id}/assembly/add', AddAssmResource())  #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/delete', DeleteAssmResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/vulnerability/{resolved}', AssemblyCveResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/joint', AssemblyJointResource()) #---
app.add_route('/projects/{prj_id}/assembly/{assm_id}/compare', AssemblyCompareResource()) #--
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package', PackageResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/vulnerability/{resolved}', PackageCveResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/joint/{pkg_vul_id}/vulnerability/{resolved}', JointCveResource()) #--
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/changelog', ChangelogResource()) #
