# Actividad SOA - Plataforma Unificada (Fase 1)

Entrega completa de una plataforma unificada de servicios académicos con arquitectura orientada a servicios (SOA) integrando APIs SOAP y REST.

## Entregables

1. **`db_schema.sql`** — Modelo de BD MySQL (tablas: students, courses, enrollments, grades).
2. **`soap_service/app.py`** — Servicio SOAP con operaciones GetEnrollments y CreateEnrollment (Puerto 5000).
3. **`rest_service_py/app.py`** — Servicio REST con endpoints para grades, students, courses (Puerto 5001).
4. **`postman/UAU_collection.json`** — Colección de Postman con 8 ejemplos de prueba (SOAP y REST).
5. **`db_test.py`, `migrate_db_fixed.py`** — Scripts para diagnosticar y migrar esquema BD.
6. **`insert_test_data.py`** — Script para insertar datos de prueba.

## Arquitectura

```
┌─────────────────────┐
│   Cliente Web       │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼───┐    ┌───▼────┐
│ SOAP  │    │ REST   │
│ (5000)│    │ (5001) │
└───┬───┘    └───┬────┘
    │            │
    └───────┬────┘
            │
        ┌───▼───────┐
        │  MySQL    │
        │  Railway  │
        └───────────┘
```

## Configuración de BD (Railway)

URL de conexión (usada en los servicios):
```
mysql://root:CHZNvnVxlJVQtyjruZmbLsXnDitHWSTH@shuttle.proxy.rlwy.net:22345/railway
```

## Instalación y Ejecución Rápida

### 1. Prerequisitos

- Python 3.11+
- MySQL (Railway ya configurado)

### 2. Preparar Entorno

```powershell
cd 'C:\Users\filib\Documents\Actividad'

# Crear entorno virtual
python -m venv .venv

# Activar venv (si necesario para instalar deps por separado)
# .\.venv\Scripts\Activate.ps1

# Instalar dependencias
.\.venv\Scripts\python.exe -m pip install -r soap_service\requirements.txt
.\.venv\Scripts\python.exe -m pip install lxml
```

### 3. Migrar BD e Insertar Datos

```powershell
$env:DATABASE_URL = "mysql://root:CHZNvnVxlJVQtyjruZmbLsXnDitHWSTH@shuttle.proxy.rlwy.net:22345/railway"

# Crear tablas
.\.venv\Scripts\python.exe migrate_db_fixed.py

# Insertar datos de prueba
.\.venv\Scripts\python.exe insert_test_data.py

# Verificar
.\.venv\Scripts\python.exe db_test.py
```

### 4. Ejecutar Servicios

**Terminal 1 - SOAP:**
```powershell
cd 'C:\Users\filib\Documents\Actividad'
$env:DATABASE_URL = "mysql://root:CHZNvnVxlJVQtyjruZmbLsXnDitHWSTH@shuttle.proxy.rlwy.net:22345/railway"
.\.venv\Scripts\python.exe soap_service\app.py
```
Endpoint: `http://localhost:5000/soap`

**Terminal 2 - REST:**
```powershell
cd 'C:\Users\filib\Documents\Actividad'
$env:DATABASE_URL = "mysql://root:CHZNvnVxlJVQtyjruZmbLsXnDitHWSTH@shuttle.proxy.rlwy.net:22345/railway"
.\.venv\Scripts\python.exe rest_service_py\app.py
```
Endpoints: `http://localhost:5001/api/{grades|students|courses}`

## API SOAP (Enrollments)

### GetEnrollments

**Request:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetEnrollments>
      <student_id>1</student_id>
    </GetEnrollments>
  </soap:Body>
</soap:Envelope>
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetEnrollmentsResponse>
      <enrollment>
        <id>1</id>
        <student_id>1</student_id>
        <course_id>1</course_id>
        <status>enrolled</status>
      </enrollment>
    </GetEnrollmentsResponse>
  </soap:Body>
</soap:Envelope>
```

### CreateEnrollment

**Request:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateEnrollment>
      <student_id>2</student_id>
      <course_id>3</course_id>
      <status>enrolled</status>
    </CreateEnrollment>
  </soap:Body>
</soap:Envelope>
```

## API REST

### GET /api/grades
Listar todas las calificaciones.

**Response:**
```json
[
  { "id": 1, "enrollment_id": 1, "grade": 85.5 },
  { "id": 2, "enrollment_id": 2, "grade": 90.0 }
]
```

### POST /api/grades
Crear nueva calificación.

**Body:**
```json
{ "enrollment_id": 1, "grade": 88.5 }
```

### GET /api/students
Listar estudiantes.

### POST /api/students
Crear estudiante.

**Body:**
```json
{
  "student_number": "20230004",
  "first_name": "Ana",
  "last_name": "Martínez",
  "email": "ana@uav.edu.mx"
}
```

### GET /api/courses
Listar cursos.

### POST /api/courses
Crear curso.

**Body:**
```json
{
  "code": "QUI101",
  "name": "Química I",
  "credits": 4
}
```

## Pruebas con Postman

1. Abre Postman.
2. Importa la colección: `postman/UAU_collection.json`.
3. Ejecuta los 8 ejemplos (SOAP y REST).

## Archivos Principales

```
Actividad/
├── README.md                    # Este archivo
├── db_schema.sql                # Esquema de BD
├── db_test.py                   # Diagnóstico de conexión
├── migrate_db_fixed.py          # Migración de BD
├── insert_test_data.py          # Datos de prueba
├── soap_service/
│   ├── app.py                   # Servicio SOAP
│   └── requirements.txt          # Dependencias Python
├── rest_service_py/
│   └── app.py                   # Servicio REST
├── rest_service/                # Servicio REST Java (opcional)
│   ├── pom.xml
│   └── src/...
└── postman/
    └── UAU_collection.json      # Colección de Postman
```

## Notas de Seguridad

⚠️ **La contraseña de la base de datos está en este README y en el código. En producción:**
- Usa variables de entorno para credenciales.
- Cambia la contraseña en Railway después de las pruebas.
- No hagas push de credenciales a repositorios públicos.

## Requisitos Cumplidos

✅ Integración de servicios SOAP y APIs RESTful modernas.
✅ Arquitectura escalable basada en microservicios.
✅ Interoperabilidad XML (SOAP) y JSON (REST).
✅ Frontend unificado (potencial) con ambas APIs disponibles.
✅ Análisis y diseño de BD considerando múltiples módulos.
✅ Diseño de arquitectura unificada (SOAP + REST).
✅ Implementación de API SOAP (Python).
✅ Implementación de API REST (Python).
✅ Reporte de pruebas (Postman).
✅ Repositorio del proyecto (en progreso).

---

Contacto y soporte: Universidad Autónoma Veracruzana (UAU) - Actividad SOA 2025.
