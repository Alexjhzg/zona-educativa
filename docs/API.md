# Documentación de API REST — Zona Educativa

La API está construida con **FastAPI** (`backend/app/main.py`) y expone documentación interactiva automática en runtime:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **Esquema OpenAPI JSON:** `/openapi.json`

---

## 1. Salud del Servicio

| Método | Ruta | Auth | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Pública | Verifica disponibilidad del servicio (`{"status": "ok", "service": "Zona Educativa QR API", "version": "1.0.0"}`). |

---

## 2. Autenticación Admin (`/api/auth`)

Definido en [`backend/app/routers/auth.py`](../backend/app/routers/auth.py).

| Método | Ruta | Auth | Cuerpo / Parámetros | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Pública | `application/x-www-form-urlencoded` (`username`, `password`) | `Token` (`access_token`, `token_type`, `username`) |

---

## 3. Planteles Públicos (`/api/planteles`)

Definido en [`backend/app/routers/planteles.py`](../backend/app/routers/planteles.py).

| Método | Ruta | Auth | Parámetros | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/planteles/municipios` | Pública | — | `List[str]` (municipios únicos ordenados en mayúsculas) |
| `GET` | `/api/planteles/search` | Pública | `q` (`min_length=2`), `limit` (default `20`, max `100`) | `List[PlantelResponse]` |
| `GET` | `/api/planteles/dea/{query_key}` | Pública | `query_key` (Código DEA o Cédula del Director) | `PlantelResponse` (`404` si no existe) |
| `GET` | `/api/planteles/{plantel_id}` | Pública | `plantel_id: int` | `PlantelResponse` (`404` si no existe) |

---

## 4. Solicitudes QR (`/api/solicitudes`)

Definido en [`backend/app/routers/solicitudes.py`](../backend/app/routers/solicitudes.py).

| Método | Ruta | Auth | Cuerpo | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/solicitudes` | Bearer JWT (`get_current_admin`) | — | `List[SolicitudResponse]` ordenadas por `fecha_solicitud DESC` |
| `POST` | `/api/solicitudes` | Pública | `SolicitudCreate` | `201 Created` (`SolicitudResponse`) |
| `PATCH` | `/api/solicitudes/{solicitud_id}/estatus` | Bearer JWT (`get_current_admin`) | `EstatusUpdateSchema` (`estatus` o `nuevo_estatus`) | `{message, id, estatus}`. Si pasa a `PROCESADO` o `COMPLETADO`, actualiza `Plantel.estatus_qr = "QR SEGEN"`. |

---

## 5. Dashboard Analítico (`/api/dashboard`)

Definido en [`backend/app/routers/dashboard.py`](../backend/app/routers/dashboard.py).

| Método | Ruta | Auth | Cuerpo | Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/dashboard/kpis` | Bearer JWT (`get_current_admin`) | — | `DashboardKpiSummary` (totales, dependencias, `ranking_roles`, `estatus_qr_breakdown`, `municipios_summary`) |
| `GET` | `/api/dashboard/solicitudes` | Bearer JWT (`get_current_admin`) | — | `List[SolicitudResponse]` |
| `PATCH` | `/api/dashboard/solicitudes/{solicitud_id}/estatus` | Bearer JWT (`get_current_admin`) | `{"nuevo_estatus": "..."}` | `{message, solicitud_id, nuevo_estatus}` |

---

## 6. Administración de Tablas / Excel Grid (`/api/admin/data`)

Definido en [`backend/app/routers/admin_data.py`](../backend/app/routers/admin_data.py). **Todos los endpoints requieren Bearer JWT (`get_current_admin`).**

Tablas soportadas en `{table_name}`: `planteles`, `solicitudes_qr`, `municipios`.

| Método | Ruta | Parámetros / Cuerpo | Respuesta |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/admin/data/download-template/{table_name}` | `table_name` (default `planteles`) | Archivo binario `.xlsx` |
| `POST` | `/api/admin/data/{table_name}/upload-excel` | `multipart/form-data` (`file`: `.xlsx`/`.xlsm`/`.xls`/`.csv`) | `{message, backup_file, detalles}` |
| `POST` | `/api/admin/data/import-excel` | Alias de carga masiva para `planteles` | `{message, backup_file, detalles}` |
| `GET` | `/api/admin/data/{table_name}` | `q`, `skip` (>=0), `limit` (1..10000) | `{total, skip, limit, items}` |
| `PATCH` | `/api/admin/data/{table_name}/{row_id}` | `{"column": "...", "value": ...}` | `{message, id, column, value}` |
| `POST` | `/api/admin/data/{table_name}` | Diccionario JSON con campos del modelo | `{message, id}` |
| `DELETE` | `/api/admin/data/{table_name}/{row_id}` | — | `{message, id}` |
| `POST` | `/api/admin/data/{table_name}/bulk-delete` | `{"ids": [1, 2, ...]}` | `{message, ids}` |

