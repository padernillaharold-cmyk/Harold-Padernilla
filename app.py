import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))


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
