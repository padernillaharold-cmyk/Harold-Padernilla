import sqlite3
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/classmate/students')
def get_classmate_students():
    api_url = request.args.get('url', '').strip()
    if not api_url:
        return jsonify({"error": "Classmate API URL is required"}), 400
    parsed_url = urlparse(api_url)
    if parsed_url.scheme not in ('http', 'https') or not parsed_url.netloc:
        return jsonify({"error": "Enter a complete http:// or https:// API URL"}), 400

    try:
        response = requests.get(api_url, timeout=15, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        return jsonify({"error": "Unable to retrieve classmate records", "details": str(error)}), 502
    except ValueError:
        return jsonify({"error": "Classmate API did not return valid JSON"}), 502

    if not isinstance(data, list):
        return jsonify({"error": "Classmate API must return a JSON list"}), 502
    return jsonify(data)


@app.route('/api/students', methods=['GET'])
def api_get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY id').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True) or {}
    required = ('student_id', 'name', 'program', 'year', 'section')
    if any(key not in data or data[key] in ('', None) for key in required):
        return jsonify({"error": "All student fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO students (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Student added", "id": new_id}), 201


@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))


@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True) or {}
    required = ('student_id', 'name', 'program', 'year', 'section')
    if any(key not in data or data[key] in ('', None) for key in required):
        return jsonify({"error": "All student fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        """UPDATE students SET student_id = ?, name = ?, program = ?,
        year = ?, section = ? WHERE id = ?""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'], id)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student updated"})


@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted"})


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00239",
        "name": "Harold Padernilla",
        "program": "BSIT",
        "year": 3,
        "section": "B",
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!",
    })


@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_name": "System Integration",
        "program": "BSIT",
        "year_level": 3,
    })


@app.route('/Welcome')
def say_Welcome():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Welcome, {name}! from BSIT 3B Dijkstra ",
    })


if __name__ == '__main__':
    app.run(debug=True)
