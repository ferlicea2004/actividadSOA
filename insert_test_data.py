"""
Script para insertar datos de prueba en la BD.
"""
import os
import re
import mysql.connector


def parse_mysql_url(url):
    m = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', url)
    if not m:
        raise ValueError('DATABASE_URL no válido')
    return dict(user=m.group(1), password=m.group(2), host=m.group(3), port=int(m.group(4)), database=m.group(5))


DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print('Error: Define DATABASE_URL')
    exit(2)

cfg = parse_mysql_url(DATABASE_URL)
cfg['charset'] = 'utf8'

conn = mysql.connector.connect(**cfg)
cur = conn.cursor()

# Insertar estudiantes
students = [
    ('20230001', 'Juan', 'Pérez', 'juan@uav.edu.mx'),
    ('20230002', 'María', 'González', 'maria@uav.edu.mx'),
    ('20230003', 'Carlos', 'López', 'carlos@uav.edu.mx'),
]
for s in students:
    try:
        cur.execute('INSERT INTO students (student_number, first_name, last_name, email) VALUES (%s, %s, %s, %s)', s)
    except:
        pass  # Saltar duplicados

# Insertar cursos
courses = [
    ('MAT101', 'Cálculo I', 4),
    ('INF201', 'Programación Orientada a Objetos', 3),
    ('FIS101', 'Física I', 4),
]
for c in courses:
    try:
        cur.execute('INSERT INTO courses (code, name, credits) VALUES (%s, %s, %s)', c)
    except:
        pass

# Insertar matrículas
enrollments = [
    (1, 1, 'enrolled'),
    (1, 2, 'enrolled'),
    (2, 1, 'enrolled'),
    (3, 3, 'enrolled'),
]
for e in enrollments:
    try:
        cur.execute('INSERT INTO enrollments (student_id, course_id, status) VALUES (%s, %s, %s)', e)
    except:
        pass

# Insertar calificaciones
grades = [
    (1, 85.5),
    (2, 90.0),
    (3, 78.5),
    (4, 92.0),
]
for g in grades:
    try:
        cur.execute('INSERT INTO grades (enrollment_id, grade) VALUES (%s, %s)', g)
    except:
        pass

conn.commit()
cur.close()
conn.close()

print('Datos de prueba insertados correctamente.')
