# Arquitectura del Sistema — Zona Educativa

Este documento detalla la arquitectura real de **Zona Educativa** mediante diagramas C4, flujos críticos, topología de despliegue y Registros de Decisiones de Arquitectura (ADRs). Complementa el documento raíz [`ARCHITECTURE.md`](../ARCHITECTURE.md).

---

## 1. Diagrama C4 — Nivel 1: Contexto del Sistema

```mermaid
flowchart LR
    Solicitante["Solicitante Público\n(Director / Enlace SEGEN / Supervisor / Representante)"]
    Admin["Administrador\n(Zona Educativa)"]
    Excel["Archivo Fuente\nPLANTELES EDUCATIVOS - copia.xlsm"]

    subgraph Sistema["Zona Educativa (QR & Dashboard)"]
        App["Plataforma Web\nVue 3 + FastAPI + PostgreSQL"]
    end

    Solicitante -->|"Consulta plantel y registra solicitud QR (HTTP/HTTPS)"| App
    Admin -->|"Autenticación JWT, Dashboard KPIs y Data Grid"| App
    Excel -->|"Ingesta inicial (seed_data.py) y carga masiva"| App
```

---

## 2. Diagrama C4 — Nivel 2: Contenedores

```mermaid
flowchart TD
    Browser["Navegador Web"] -->|":8080 HTTP"| Nginx["Frontend Container\nNginx + Vue 3 SPA (Vite)"]
    Nginx -->|"Archivos estáticos /index.html"| Browser
    Nginx -->|"/api/* proxy_pass"| Backend["Backend Container\nFastAPI + Uvicorn (:8000)"]

    Backend -->|"SQLAlchemy ORM"| DB[("PostgreSQL 16 Alpine\n(:5432 interno / :5433 host)\no SQLite local")]
    Backend -->|"openpyxl / pandas"| Backups["Volumen /app/backups\nRespaldos automáticos"]
    Backend -->|"Background thread"| Cron["cron_cleaner.py\nLimpieza periódica"]
```

---

## 3. Flujos Clave

### 3.1 Flujo de Solicitud Pública de QR y Aprobación

```mermaid
sequenceDiagram
    actor S as Solicitante
    participant FE as Vue 3 (SolicitudView)
    participant API as FastAPI
    participant DB as Base de Datos

    S->>FE: Busca plantel por DEA / Cédula / Nombre
    FE->>API: GET /api/planteles/search?q=...
    API->>DB: Consulta Plantel (ILIKE)
    DB-->>API: Lista de planteles
    API-->>FE: PlantelResponse[]

    S->>FE: Envía formulario de solicitud QR
    FE->>API: POST /api/solicitudes
    API->>DB: Inserta SolicitudQR (estatus = PENDIENTE)
    DB-->>API: Solicitud creada
    API-->>FE: 201 Created

    Note over FE,DB: Posteriormente, un Administrador autenticado procesa la solicitud
    FE->>API: PATCH /api/dashboard/solicitudes/{id}/estatus (Bearer JWT)
    API->>DB: Actualiza SolicitudQR y, si es PROCESADO/COMPLETADO, Plantel.estatus_qr = "QR SEGEN"
    API-->>FE: 200 OK
```

### 3.2 Flujo de Carga Masiva Excel con Respaldo Atómico

```mermaid
sequenceDiagram
    actor A as Administrador
    participant Grid as ExcelDataGrid.vue
    participant API as admin_data.py
    participant Bkp as backup_service.py
    participant ETL as excel_importer.py
    participant DB as Base de Datos

    A->>Grid: Sube archivo .xlsx/.xlsm/.csv
    Grid->>API: POST /api/admin/data/{table_name}/upload-excel (Bearer JWT)
    API->>Bkp: create_table_backup(db, table_name)
    Bkp-->>API: Ruta archivo de respaldo
    API->>ETL: process_excel_import(contents, db)
    ETL->>DB: Upsert de registros por codigo_dea
    DB-->>ETL: Commit
    ETL-->>API: Resumen de importación
    API-->>Grid: 200 OK (backup_file + detalles)
```

---

## 4. Topología de Despliegue (`docker-compose.yml`)

| Servicio | Contenedor | Imagen / Build | Puertos (Host:Contenedor) | Persistencia |
| :--- | :--- | :--- | :--- | :--- |
| `db` | `zona_educativa_db` | `postgres:16-alpine` | `5433:5432` | Volumen `postgres_data` |
| `backend` | `zona_educativa_backend` | `./backend/Dockerfile` | `8000:8000` | Bind `./backend:/app` + `.xlsm` |
| `frontend` | `zona_educativa_frontend` | `./frontend/Dockerfile` | `8080:80` | Bind `./frontend/dist` y `nginx.conf` |

- **Arranque del backend:** `python app/seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000` tras verificar `service_healthy` en `db`.
- **Proxy inverso:** `frontend/nginx.conf` sirve la SPA con `try_files $uri $uri/ /index.html` y redirige `/api/` a `http://backend:8000/api/`.

---

## 5. Registros de Decisiones de Arquitectura (ADRs)

### ADR-001: FastAPI + SQLAlchemy 2.0 con doble soporte PostgreSQL / SQLite
- **Contexto:** Se requiere una API rápida con validación tipada y facilidad de pruebas locales sin depender de un servidor PostgreSQL en cada estación.
- **Decisión:** Usar FastAPI, Pydantic v2 y SQLAlchemy leyendo `DATABASE_URL` con fallback a `sqlite:///./zona_educativa.db` (`backend/app/database.py`).
- **Consecuencias:** Permite ejecutar pruebas y desarrollo local rápidamente, manteniendo PostgreSQL 16 en Docker/producción.

### ADR-002: Vue 3 (Composition API) + Pinia + AG Grid
- **Contexto:** El panel administrativo necesita manipular ~988 planteles con edición por celda, filtros y exportación/importación.
- **Decisión:** Adoptar Vue 3 `<script setup>`, Pinia para estado global (`stores/`), composables reutilizables (`composables/`) y `ag-grid-vue3` para la vista tabular.
- **Consecuencias:** Alta interactividad en el navegador y separación clara entre lógica de estado y presentación.

### ADR-003: Respaldo previo obligatorio en importaciones Excel
- **Contexto:** Una carga masiva defectuosa podría sobrescribir registros válidos de planteles.
- **Decisión:** Invocar `create_table_backup(db, table_name)` antes de ejecutar `process_excel_import` en `admin_data.py`. Si el respaldo falla, la importación se aborta con HTTP 500.
- **Consecuencias:** Protege la integridad histórica de los datos ante errores humanos durante cargas masivas.

