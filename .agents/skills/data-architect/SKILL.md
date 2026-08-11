---
name: data-architect
description: Especialista en ingesta de datos, ETL y modelado de datos para el archivo PLANTELES EDUCATIVOS XLSM y base de datos relacional.
---

# Skill: Data Architect & ETL Specialist

Este skill guía la ingesta, limpieza, normalización y migración de datos desde archivos Excel (`.xlsm`) hacia la base de datos relacional (PostgreSQL/SQLite).

## Responsabilidades Principales:
1. **Inspección e Ingesta del Excel**:
   - Usar `pandas` y `openpyxl` para extraer las 34 columnas del sheet `planteles`.
   - Limpiar espacios en blanco adicionales con `.strip()` en todas las columnas de texto.
   - Estandarizar valores categóricos (ej. `'PRIVADA '`, `' ESTADAL'`, `'NACIONAL '` -> `'PRIVADA'`, `'ESTADAL'`, `'NACIONAL'`).

2. **Modelado Relacional (SQLAlchemy)**:
   - Tabla `municipios`: ID, nombre.
   - Tabla `parroquias`: ID, municipio_id, nombre.
   - Tabla `planteles`: ID, codigo_dea, plantel, dependencia, denominacion, direccion, comunidad, rol_contacto, nombres_contacto, ci_contacto, telefono_contacto, email_contacto, estatus_zona, estatus_segen, estatus_director, estatus_qr, qr_segen, qr_director, latitud, longitud, precision.
   - Tabla `solicitudes_qr`: ID, plantel_id, tipo_solicitud (NUEVO_ASIGNACION, REPOSICION, CORRECCION), solicitante_nombre, solicitante_ci, solicitante_telefono, solicitante_email, solicitante_rol (DIRECTOR, SEGEN, ZONA_EDUCATIVA, SUPERVISOR), motivo, estatus_solicitud, fecha_solicitud.

3. **Garantía de Calidad**:
   - Evitar duplicados por `CODIGO PLANTEL` (DEA).
   - Generar logs claros durante el proceso de migración de los 988 registros.
