"""
Servicio REST en Python (Flask).
Expone API para grades y students.
"""
import os
import re
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)


def parse_mysql_url(url):
    m = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', url)
    if not m:
        raise ValueError('DATABASE_URL no válido')
    return dict(user=m.group(1), password=m.group(2), host=m.group(3), port=int(m.group(4)), database=m.group(5))


DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('Setear variable de entorno DATABASE_URL')
DB_CONFIG = parse_mysql_url(DATABASE_URL)
DB_CONFIG['charset'] = 'utf8'


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route('/api/grades', methods=['GET'])
def list_grades():
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, enrollment_id, grade FROM grades')
        grades = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(grades)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grades', methods=['POST'])
def create_grade():
    try:
        data = request.get_json()
        enrollment_id = data.get('enrollment_id')
        grade = data.get('grade')
        
        if not enrollment_id or grade is None:
            return jsonify({'error': 'Missing enrollment_id or grade'}), 400
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO grades (enrollment_id, grade) VALUES (%s, %s)', (enrollment_id, grade))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify({'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['GET'])
def list_students():
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, student_number, first_name, last_name, email FROM students')
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        student_number = data.get('student_number')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        
        if not student_number or not first_name or not last_name:
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO students (student_number, first_name, last_name, email) VALUES (%s, %s, %s, %s)',
                   (student_number, first_name, last_name, email))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify({'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses', methods=['GET'])
def list_courses():
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, code, name, credits FROM courses')
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses', methods=['POST'])
def create_course():
    try:
        data = request.get_json()
        code = data.get('code')
        name = data.get('name')
        credits = data.get('credits', 3)
        
        if not code or not name:
            return jsonify({'error': 'Missing code or name'}), 400
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO courses (code, name, credits) VALUES (%s, %s, %s)', (code, name, credits))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify({'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('Servicio REST escuchando en http://0.0.0.0:5001/api')
    app.run(host='0.0.0.0', port=5001, debug=False)
