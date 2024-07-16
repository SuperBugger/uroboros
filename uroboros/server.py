# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from api.query_commands.project_query import ProjectApi
from api.query_commands.assembly_query import AssemblyApi
from api.query_commands.package_query import PackageApi
from configure import NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB
from connection import DbHelper

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

project_api = ProjectApi(DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB))
assembly_api = AssemblyApi(DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB))
package_api = PackageApi(DbHelper(NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB))


@app.route('/')
def index():
    return "Welcome to the Package API"


@app.route('/delete_table', methods=['POST'])
def delete_table():
    data = request.json
    table_name = data.get('table_name')
    if not table_name:
        return jsonify({'error': 'table_name is required'}), 400

    try:
        package_api.delete_table(table_name)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/joint_assm', methods=['POST'])
def joint_assm():
    data = request.json
    assm_id = data.get('assm_id')
    if not assm_id:
        return jsonify({'error': 'assm_id is required'}), 400

    try:
        package_api.joint_assm(data)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_difference', methods=['POST'])
def get_difference():
    data = request.json
    assm_id = data.get('assm_id')
    if not assm_id:
        return jsonify({'error': 'assm_id is required'}), 400

    try:
        package_api.get_difference(data)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_projects', methods=['GET'])
def get_projects():
    try:
        projects = project_api.get_projects()
        return jsonify({'projects': projects}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/<project_name>/get_assemblies', methods=['GET'])
def get_assemblies(project_name):
    try:
        prj_id_query = "SELECT prj_id FROM repositories.project WHERE prj_name = %s"
        prj_id_result = db_helper.query(prj_id_query, (project_name,))
        if not prj_id_result:
            return jsonify({'error': 'Project not found'}), 404

        prj_id = prj_id_result[0][0]

        assemblies = assembly_api.run(prj_id)
        return jsonify({'assemblies': assemblies}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/<project_name>/assemblies', methods=['GET'])
def assemblies_page(project_name):
    return render_template('assembly.html', project_name=project_name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
