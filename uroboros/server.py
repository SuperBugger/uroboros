# app.py
from flask import Flask, request, jsonify
from api.query_commands.package_query import PackageApi
from configure import NAME_DB, USER_DB, PASSWORD_DB, HOST_DB, PORT_DB
from connection import DbHelper

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
