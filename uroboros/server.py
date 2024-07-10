from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_SETTINGS = {
    'dbname': 'uroboros',
    'user': 'owner',
    'password': '1111',
    'host': 'localhost',
    'port': '5432'
}


def get_db_connection():
    conn = psycopg2.connect(**DB_SETTINGS)
    return conn


@app.route('/api/data/<section_id>', methods=['GET'])
def get_data(section_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = f"SELECT * FROM {section_id};"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
