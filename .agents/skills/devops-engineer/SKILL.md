---
name: devops-engineer
description: Especialista DevOps para orquestación en Docker, Docker Compose, Nginx, variables de entorno y preparación para despliegue en servidor.
---

# Skill: DevOps & Infrastructure Engineer

Este skill asegura que toda la infraestructura containerizada esté lista para desarrollo y producción.

## Responsabilidades Principales:
1. **Dockerfile Backend**:
   - Base Python 3.11-slim.
   - Instalación optimizada de dependencias (`requirements.txt`).
   - Ejecución mediante `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

2. **Dockerfile Frontend Multi-Stage**:
   - Stage 1: Build estático con Node.js 20 (`npm run build`).
   - Stage 2: Servidor Nginx Alpine sirviendo `/dist` y proxying `/api` al backend.

3. **Orquestación `docker-compose.yml`**:
   - Servicios: `db` (PostgreSQL 16), `backend`, `frontend`.
   - Healthchecks para esperar que la BD esté lista antes de lanzar FastAPI.
   - Volúmenes persistentes para PostgreSQL.
   - Red interna aislada `zona-educativa-net`.
