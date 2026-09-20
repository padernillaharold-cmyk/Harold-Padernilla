from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to my first API!"
@app.route('/student')
def get_student():
    return jsonify({
"student_id": "24-00239",
"name": "Harold Padernilla",
"program": "BSIT",
"year": 3,
"section": "B"
})
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
"message": f"Hello, {name}!"
})

@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_name": "System Integration",
        "program": "BSIT",
        "year_level": 3
})

@app.route('/Welcome')
def say_Welcome():
    name = request.args.get('name', 'Student')
    return jsonify({
"message": f"Welcome, {name}! "
})

if __name__ == '__main__':
    app.run(debug=True)

