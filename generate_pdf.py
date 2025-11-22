"""
Script para generar PDF del informe de arquitectura.
Usa reportlab para convertir Markdown a PDF.
"""
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors


def md_to_pdf():
    filename = 'ARQUITECTURA_SOA_INFORME.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter, 
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#004d99'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    story = []
    
    # Portada
    story.append(Paragraph('Informe de Diseño', title_style))
    story.append(Paragraph('Plataforma Unificada de Servicios Académicos (SOA)', heading1_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('Universidad Autónoma Veracruzana', normal_style))
    story.append(Paragraph('Actividad: Arquitectura Orientada a Servicios', normal_style))
    story.append(Paragraph('Fecha: Noviembre 22, 2025', normal_style))
    story.append(Paragraph('Versión: 1.0', normal_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Introducción
    story.append(Paragraph('1. Introducción', heading1_style))
    story.append(Paragraph(
        'La Universidad Autónoma Veracruzana enfrenta una crisis de integración tecnológica entre sus sistemas desacoplados. '
        'Este informe presenta el diseño e implementación de la Fase 1 de una plataforma web unificada basada en arquitectura '
        'orientada a servicios (SOA).',
        normal_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Problema
    story.append(Paragraph('2. Análisis del Problema', heading1_style))
    story.append(Paragraph('2.1 Sistemas Existentes', heading2_style))
    story.append(Paragraph('• Sistema de Matrículas: SOAP parcialmente, base de datos MySQL local.', normal_style))
    story.append(Paragraph('• Plataforma de Cursos Online: API REST aislada, sin integración.', normal_style))
    story.append(Paragraph('• Sistema de Calificaciones: Base de datos independiente, exports manuales en múltiples formatos.', normal_style))
    story.append(Paragraph('• Aplicación Móvil: Sin integración completa.', normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph('2.2 Desafíos Identificados', heading2_style))
    story.append(Paragraph('• Duplicación de datos entre sistemas', normal_style))
    story.append(Paragraph('• Procesos manuales para sincronización', normal_style))
    story.append(Paragraph('• Falta de interoperabilidad XML/JSON', normal_style))
    story.append(Paragraph('• Escalabilidad limitada', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Solución
    story.append(Paragraph('3. Solución Propuesta: SOA', heading1_style))
    story.append(Paragraph('3.1 Principios de Diseño', heading2_style))
    story.append(Paragraph('1. <b>Independencia de Servicios</b>: Cada módulo es un servicio autónomo.', normal_style))
    story.append(Paragraph('2. <b>Interoperabilidad</b>: Soporte de SOAP (XML) y REST (JSON).', normal_style))
    story.append(Paragraph('3. <b>Escalabilidad</b>: Basado en microservicios, permite crecimiento horizontal.', normal_style))
    story.append(Paragraph('4. <b>Reutilización</b>: APIs expuestas para múltiples consumidores.', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph('3.2 Componentes de la Arquitectura', heading2_style))
    story.append(Paragraph('<b>Servicio SOAP - Enrollments (Matrículas)</b>', normal_style))
    story.append(Paragraph('• Puerto: 5000', normal_style))
    story.append(Paragraph('• Protocolo: SOAP 1.1 / XML', normal_style))
    story.append(Paragraph('• Operaciones: GetEnrollments, CreateEnrollment', normal_style))
    story.append(Paragraph('• Implementación: Python (Flask + lxml)', normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph('<b>Servicio REST - Grades, Students, Courses</b>', normal_style))
    story.append(Paragraph('• Puerto: 5001', normal_style))
    story.append(Paragraph('• Protocolo: HTTP REST / JSON', normal_style))
    story.append(Paragraph('• Endpoints: /api/grades, /api/students, /api/courses', normal_style))
    story.append(Paragraph('• Implementación: Python (Flask)', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Base de datos
    story.append(Paragraph('4. Modelo de Datos', heading1_style))
    story.append(Paragraph('Base de Datos MySQL (Railway)', heading2_style))
    story.append(Paragraph('• Host: shuttle.proxy.rlwy.net:22345', normal_style))
    story.append(Paragraph('• Nombre: railway', normal_style))
    story.append(Paragraph('• Tablas: students, courses, enrollments, grades', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Tablas
    data = [
        ['Tabla', 'Columnas', 'Relación'],
        ['students', 'id, student_number, first_name, last_name, email', 'PK'],
        ['courses', 'id, code, name, credits', 'PK'],
        ['enrollments', 'id, student_id (FK), course_id (FK), enrolled_at, status', 'PK, FK'],
        ['grades', 'id, enrollment_id (FK), grade, graded_at', 'PK, FK']
    ]
    
    table = Table(data, colWidths=[1.2*inch, 2.5*inch, 1.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.15*inch))
    
    # Decisiones técnicas
    story.append(PageBreak())
    story.append(Paragraph('5. Decisiones Técnicas', heading1_style))
    story.append(Paragraph(
        '<b>SOAP:</b> Python + Flask + lxml (ligero, fácil de mantener, compatible con XML/SOAP)<br/>'
        '<b>REST:</b> Python + Flask (consistencia con SOAP, simplicidad operacional)<br/>'
        '<b>Base de Datos:</b> MySQL en Railway (acceso remoto, escalabilidad, compatibilidad)<br/>'
        '<b>Formatos:</b> SOAP (XML) + REST (JSON) para interoperabilidad máxima<br/>'
        '<b>Autenticación:</b> Ninguna en Fase 1 (implementar en Fase 2)',
        normal_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Casos de Uso
    story.append(Paragraph('6. Casos de Uso', heading1_style))
    story.append(Paragraph('<b>UC1: Consultar Matrículas (SOAP)</b>', normal_style))
    story.append(Paragraph('1. Sistema envía petición SOAP con student_id', normal_style))
    story.append(Paragraph('2. Servicio consulta tabla enrollments', normal_style))
    story.append(Paragraph('3. Retorna XML con enrollments del estudiante', normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph('<b>UC2: Registrar Calificación (REST)</b>', normal_style))
    story.append(Paragraph('1. Portal envía POST a /api/grades', normal_style))
    story.append(Paragraph('2. Servicio inserta en tabla grades', normal_style))
    story.append(Paragraph('3. Retorna JSON con ID de nueva calificación', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Fases futuras
    story.append(Paragraph('7. Plan de Implementación Posterior', heading1_style))
    story.append(Paragraph('<b>Fase 2: Mejoras</b>', normal_style))
    story.append(Paragraph('• Autenticación y autorización (OAuth2, JWT)', normal_style))
    story.append(Paragraph('• Validación de datos avanzada', normal_style))
    story.append(Paragraph('• Logging y monitoreo', normal_style))
    story.append(Paragraph('• Rate limiting', normal_style))
    story.append(Paragraph('• Documentación de API (Swagger/OpenAPI)', normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph('<b>Fase 3: Escalabilidad</b>', normal_style))
    story.append(Paragraph('• Caché (Redis)', normal_style))
    story.append(Paragraph('• Balanceador de carga', normal_style))
    story.append(Paragraph('• Contenedores (Docker)', normal_style))
    story.append(Paragraph('• Orquestación (Kubernetes)', normal_style))
    story.append(Paragraph('• API Gateway', normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Conclusiones
    story.append(Paragraph('8. Conclusiones', heading1_style))
    story.append(Paragraph(
        'La arquitectura propuesta cumple con los requisitos de interoperabilidad, escalabilidad e integración unificada. '
        'La Fase 1 proporciona una base sólida para futuras expansiones sin necesidad de refactorización mayor.',
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        '<i>Documento generado automáticamente - Universidad Autónoma Veracruzana - Noviembre 2025</i>',
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Generar PDF
    doc.build(story)
    print(f'PDF generado: {filename}')


if __name__ == '__main__':
    md_to_pdf()
