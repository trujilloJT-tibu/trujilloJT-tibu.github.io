# SIEM Log Parser & Incident Auditor (ISO 27001 Compliance)

## 📌 Descripción del Proyecto
Este proyecto consiste en un analizador de registros (Log Parser) modular desarrollado en Python, diseñado para centralizar, auditar y detectar anomalías de red basadas en firmas de ataques comunes (SQL Injection y Fuerza Bruta). 

Los incidentes detectados son estructurados y almacenados en una base de datos relacional (SQLite) para su posterior auditoría y generación de reportes de cumplimiento normativo, alineándose con los controles de gestión de incidentes de la norma **ISO/IEC 27001** (Control A.12.4 - Registro y supervisión).

---

## 🛠️ Tecnologías y Conceptos Aplicados
* **Lenguaje de Programación:** Python 3 (Módulos nativos `re` para expresiones regulares y `sqlite3`).
* **Base de Datos:** SQL (Diseño de tablas, inserción estructurada de datos y consultas mediante `SELECT` y `ORDER BY`).
* **Ciberdefensa:** Análisis forense de logs web, detección de patrones de inyección de código (OWASP Top 10) y monitoreo de accesos anómalos.
* **Cumplimiento (Compliance):** Formateo de reportes bajo estándares de auditoría de seguridad de la información.

---

## 📁 Estructura del Repositorio
* `access.log`: Archivo de texto plano que simula los registros de auditoría de un servidor web en producción.
* `analizador.py`: Script principal que procesa el archivo de logs línea por línea, aplica las reglas de detección (firmas) e interactúa con la base de datos.
* `reporte.py`: Interfaz de consola que ejecuta consultas SQL complejas para extraer la información consolidada y presentar un reporte limpio para tomadores de decisiones o auditores.
* `ciberdefensa.db`: Base de datos relacional generada automáticamente donde se mantiene la persistencia de los incidentes.

---

## 🚀 Instrucciones de Ejecución

### 1. Procesamiento y Detección
Para iniciar el motor de análisis y alimentar la base de datos con las alertas detectadas, ejecute:
```bash
python analizador.py