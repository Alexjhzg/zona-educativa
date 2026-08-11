---
name: fastapi-developer
description: Desarrollador Backend especializado en FastAPI, SQLAlchemy, Pydantic y API REST para gestión de QR y agregación de KPIs.
---

# Skill: FastAPI Backend Developer

Este skill define las pautas para construir la API REST asíncrona en Python con FastAPI.

## Responsabilidades Principales:
1. **Modelos y Schemas**:
   - Modelos SQLAlchemy bien tipados con relaciones relacionales (`relationship`).
   - Esquemas Pydantic V2 para request body y response body con validaciones estrictas.

2. **Endpoints de Solicitudes (`/api/solicitudes`)**:
   - `POST /api/solicitudes`: Crear nueva solicitud de QR con validaciones (cédula, correo, tipo de solicitud).
   - `GET /api/solicitudes`: Listar solicitudes con paginación y filtros.
   - `GET /api/planteles`: Autocompletado y búsqueda de planteles por código DEA, municipio o nombre.

3. **Endpoints del Dashboard (`/api/dashboard`)**:
   - `GET /api/dashboard/kpis`: Métricas agregadas ultra-rápidas:
     - Total de planteles por estatus QR.
     - Top Solicitantes por Rol (quién pide más QR).
     - Top Municipios con mayor solicitud/reposición de QR.
     - Distribución por Dependencia (Nacional, Estadal, Privada).
     - Tasa de efectividad de levantamiento SEGEN vs Director.
