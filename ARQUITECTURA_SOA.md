# Informe de Diseño: Plataforma Unificada de Servicios Académicos (SOA)

## 1. Introducción

La Universidad Autónoma Veracruzana enfrenta una crisis de integración tecnológica entre sus sistemas desacoplados. Este informe presenta el diseño e implementación de la **Fase 1** de una plataforma web unificada basada en arquitectura orientada a servicios (SOA).

## 2. Análisis del Problema

### Sistemas Existentes
- **Sistema de Matrículas**: SOAP parcialmente, base de datos MySQL local.
- **Plataforma de Cursos Online**: API REST aislada, sin integración.
- **Sistema de Calificaciones**: Base de datos independiente, exports manuales en múltiples formatos (SQL, CSV, XLSX, JSON).
- **Aplicación Móvil**: Sin integración completa.

### Desafíos
- Duplicación de datos entre sistemas.
- Procesos manuales para sincronización.
- Falta de interoperabilidad XML/JSON.
- Escalabilidad limitada.

## 3. Solución Propuesta: SOA

### 3.1 Principios de Diseño

1. **Independencia de Servicios**: Cada módulo (Enrollments, Grades) es un servicio autónomo.
2. **Interoperabilidad**: Soporte de SOAP (XML) y REST (JSON).
3. **Escalabilidad**: Basado en microservicios, permite crecimiento horizontal.
4. **Reutilización**: APIs expuestas para múltiples consumidores (web, móvil, terceros).

### 3.2 Componentes de la Arquitectura

#### Capa de Servicios

**Servicio SOAP - Enrollments (Matrículas)**
- **Puerto**: 5000
- **Protocolo**: SOAP 1.1 / XML
- **Operaciones**:
  - `GetEnrollments(student_id)` → Lista matrículas del estudiante
  - `CreateEnrollment(student_id, course_id, status)` → Registra nueva matrícula
- **Implementación**: Python (Flask + lxml)
- **Ventaja**: Compatibilidad con sistemas legados SOAP.

**Servicio REST - Grades, Students, Courses**
- **Puerto**: 5001
- **Protocolo**: HTTP REST / JSON
- **Endpoints**:
  - `GET /api/grades` → Listar calificaciones
  - `POST /api/grades` → Crear calificación
  - `GET /api/students` → Listar estudiantes
  - `POST /api/students` → Crear estudiante
  - `GET /api/courses` → Listar cursos
  - `POST /api/courses` → Crear curso
- **Implementación**: Python (Flask)
- **Ventaja**: Moderna, eficiente, fácil de consumir desde web/móvil.

#### Capa de Datos

**Base de Datos MySQL (Railway)**
- **Host**: `shuttle.proxy.rlwy.net:22345`
- **Nombre**: `railway`
- **Tablas**:
  - `students` (id, student_number, first_name, last_name, email)
  - `courses` (id, code, name, credits)
  - `enrollments` (id, student_id, course_id, enrolled_at, status)
  - `grades` (id, enrollment_id, grade, graded_at)

**Relaciones**:
```
students ──┐
           ├─→ enrollments ──→ grades
courses ───┘
```

#### Capa de Presentación

- **Web Frontend**: Puede consumir ambas APIs (SOAP vía intermediario, REST directo).
- **Aplicación Móvil**: Acceso preferente vía REST (JSON, más eficiente).
- **Terceros**: Integración vía REST o SOAP según necesidad.

### 3.3 Diagrama de Flujo

```
┌──────────────────────────────────────────────────────┐
│            Aplicaciones Cliente                      │
│  (Web, Móvil, Terceros)                             │
└────────────┬──────────────────────┬─────────────────┘
             │                      │
      ┌──────▼──────┐         ┌────▼────────┐
      │  SOAP       │         │  REST       │
      │  (5000)     │         │  (5001)     │
      │ Enrollments │         │ Grades,    │
      │             │         │ Students,  │
      │             │         │ Courses    │
      └──────┬──────┘         └────┬────────┘
             │                     │
             └──────────┬──────────┘
                        │
                   ┌────▼────────┐
                   │  MySQL      │
                   │  Railway    │
                   │  (railway)  │
                   └─────────────┘
```

## 4. Decisiones Técnicas

| Aspecto | Decisión | Justificación |
|--------|----------|---------------|
| SOAP | Python + Flask + lxml | Ligero, fácil de mantener, compatible con XML/SOAP |
| REST | Python + Flask | Consistencia con SOAP, simplicidad operacional |
| BD | MySQL en Railway | Acceso remoto, escalabilidad, compatibilidad |
| API Format | SOAP (XML) + REST (JSON) | Interoperabilidad máxima (legado + moderno) |
| Autenticación | Ninguna (Fase 1) | Fuera de scope; implementar en Fase 2 |

## 5. Modelo de Datos

### Entidad: Student
```sql
CREATE TABLE students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_number VARCHAR(30) UNIQUE NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(150)
);
```

### Entidad: Course
```sql
CREATE TABLE courses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  credits INT DEFAULT 3
);
```

### Entidad: Enrollment
```sql
CREATE TABLE enrollments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(30) DEFAULT 'enrolled',
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

### Entidad: Grade
```sql
CREATE TABLE grades (
  id INT PRIMARY KEY AUTO_INCREMENT,
  enrollment_id INT NOT NULL,
  grade DECIMAL(5,2),
  graded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
);
```

## 6. Casos de Uso

### UC1: Consultar Matrículas (SOAP)
**Actor**: Sistema Legado
**Flujo**:
1. Sistema envía petición SOAP con `student_id=1`.
2. Servicio SOAP consulta tabla `enrollments`.
3. Retorna XML con enrollments del estudiante.

### UC2: Registrar Calificación (REST)
**Actor**: Profesor (vía portal web)
**Flujo**:
1. Portal envía POST a `/api/grades` con `enrollment_id` y `grade`.
2. Servicio REST inserta en `grades`.
3. Retorna JSON con ID de nueva calificación.

### UC3: Listar Estudiantes (REST)
**Actor**: Administrador
**Flujo**:
1. Sistema envía GET a `/api/students`.
2. Servicio retorna JSON con lista de estudiantes.

## 7. Plan de Implementación Posterior (Fases 2-3)

### Fase 2: Mejoras
- [ ] Autenticación y autorización (OAuth2, JWT).
- [ ] Validación de datos (schemas, constraints).
- [ ] Logging y monitoreo.
- [ ] Rate limiting.
- [ ] Documentación de API (Swagger/OpenAPI).

### Fase 3: Escalabilidad
- [ ] Caché (Redis).
- [ ] Balanceador de carga.
- [ ] Contenedores (Docker).
- [ ] Orquestación (Kubernetes).
- [ ] API Gateway.

## 8. Conclusiones

La arquitectura propuesta cumple los requisitos de:
- ✅ Interoperabilidad entre SOAP y REST.
- ✅ Escalabilidad basada en microservicios.
- ✅ Integración unificada de múltiples módulos.
- ✅ Base de datos normalizada.
- ✅ Facilidad de mantenimiento y extensión.

La Fase 1 proporciona una base sólida para futuras expansiones sin necesidad de refactorización mayor.

---

**Documento**: Informe de Diseño SOA - Universidad Autónoma Veracruzana
**Fecha**: Noviembre 22, 2025
**Versión**: 1.0
