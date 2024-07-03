import pathlib

import falcon

from uro_app.resources import *

app = falcon.App()

STATIC_PATH = pathlib.Path(__file__).parent / 'static'
app.add_static_route('/static', str(STATIC_PATH), downloadable=True, fallback_filename=None)
#app.add_route("/projects/{prj_id}", ProjectResource()) #+
app.add_route("/projects", ProjectResource()) #+
app.add_route("/projects/add", ProjectAddResource()) #+
app.add_route('/projects/{prj_id}/assembly', AssemblyResource())  #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/vulnerability/{resolved}', AssemblyCveResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/joint', AssemblyJointResource()) #---
app.add_route('/projects/{prj_id}/assembly/{assm_id}/compare/{prev)/{current}', AssemblyCompareResource()) #--
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package', PackageResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/cve/{resolved}', PackageCveResource()) #+
app.add_route('/projects/{prj_id}/assembly/{assm_id}/joint/cve/{resolved}', JointCveResource()) #--
app.add_route('/projects/{prj_id}/assembly/{assm_id}/package/{pkg_id}/changelog', ChangelogResource()) #
