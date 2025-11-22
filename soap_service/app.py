import os
import re
import mysql.connector
from flask import Flask, request, Response
from lxml import etree


def parse_mysql_url(url):
    m = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', url)
    if not m:
        raise ValueError('DATABASE_URL no válido')
    return dict(user=m.group(1), password=m.group(2), host=m.group(3), port=int(m.group(4)), database=m.group(5))


app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('Setear variable de entorno DATABASE_URL')
DB_CONFIG = parse_mysql_url(DATABASE_URL)
DB_CONFIG['charset'] = 'utf8'


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def build_soap_response(content_xml):
    """Construir respuesta SOAP envuelta en envelope."""
    root = etree.Element(
        '{http://schemas.xmlsoap.org/soap/envelope/}Envelope',
        nsmap={'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
    )
    body = etree.SubElement(root, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
    body.append(content_xml)
    return etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)


@app.route('/soap', methods=['POST', 'GET'])
def soap_endpoint():
    if request.method == 'GET':
        wsdl = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" name="EnrollmentService">
  <message name="GetEnrollmentsRequest">
    <part name="student_id" type="xsd:int"/>
  </message>
</definitions>"""
        return Response(wsdl, mimetype='text/xml')

    try:
        body = request.get_data(as_text=True)
        root = etree.fromstring(body.encode('utf-8'))
        
        body_elem = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
        if body_elem is None:
            return Response('Invalid SOAP', status=400, mimetype='text/plain')
        
        op_elem = body_elem[0]
        op_name = op_elem.tag.split('}')[-1] if '}' in op_elem.tag else op_elem.tag
        
        if op_name == 'GetEnrollments':
            student_id_elem = op_elem.find('.//student_id')
            if student_id_elem is None:
                return Response('Missing student_id', status=400, mimetype='text/plain')
            student_id = int(student_id_elem.text)
            
            conn = get_db()
            cur = conn.cursor(dictionary=True)
            cur.execute('SELECT id, student_id, course_id, status FROM enrollments WHERE student_id = %s', (student_id,))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            resp_elem = etree.Element('GetEnrollmentsResponse')
            for row in rows:
                e = etree.SubElement(resp_elem, 'enrollment')
                etree.SubElement(e, 'id').text = str(row['id'])
                etree.SubElement(e, 'student_id').text = str(row['student_id'])
                etree.SubElement(e, 'course_id').text = str(row['course_id'])
                etree.SubElement(e, 'status').text = str(row['status'])
            
            soap_resp = build_soap_response(resp_elem)
            return Response(soap_resp, mimetype='text/xml')
        
        elif op_name == 'CreateEnrollment':
            student_id_elem = op_elem.find('.//student_id')
            course_id_elem = op_elem.find('.//course_id')
            status_elem = op_elem.find('.//status')
            
            student_id = int(student_id_elem.text) if student_id_elem is not None else None
            course_id = int(course_id_elem.text) if course_id_elem is not None else None
            status = status_elem.text if status_elem is not None else 'enrolled'
            
            if not student_id or not course_id:
                return Response('Missing student_id or course_id', status=400, mimetype='text/plain')
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO enrollments (student_id, course_id, status) VALUES (%s,%s,%s)', 
                       (student_id, course_id, status))
            conn.commit()
            new_id = cur.lastrowid
            cur.close()
            conn.close()
            
            resp_elem = etree.Element('CreateEnrollmentResponse')
            etree.SubElement(resp_elem, 'id').text = str(new_id)
            soap_resp = build_soap_response(resp_elem)
            return Response(soap_resp, mimetype='text/xml')
        
        else:
            return Response(f'Operation {op_name} not supported', status=400, mimetype='text/plain')
    
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500, mimetype='text/plain')


if __name__ == '__main__':
    print('Servicio SOAP escuchando en http://0.0.0.0:5000/soap')
    app.run(host='0.0.0.0', port=5000, debug=False)
