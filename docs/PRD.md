# Documento de Requisitos del Producto (PRD) — Zona Educativa

## 1. Resumen Ejecutivo

**Zona Educativa** es una plataforma web orientada a la gestión centralizada de planteles educativos, recepción pública de solicitudes de códigos QR, administración masiva de registros (estilo hoja de cálculo) y análisis de indicadores clave de desempeño (KPIs) en tiempo real.

El sistema nace para resolver la descentralización y desactualización de la información de más de 980 planteles educativos, permitiendo que directores, enlaces SEGEN, supervisores y representantes reporten o soliciten códigos QR mientras el equipo administrativo consolida, audita y actualiza la base de datos.

---

## 2. Objetivos del Producto

| Objetivo | Descripción | Métrica / Resultado Esperado |
| :--- | :--- | :--- |
| **Centralización de datos** | Consolidar los registros de planteles desde el archivo fuente `PLANTELES EDUCATIVOS - copia.xlsm` en una base de datos relacional. | 100 % de los planteles importados sin duplicados por `codigo_dea`. |
| **Autoservicio de solicitudes QR** | Proveer un formulario público con búsqueda inteligente para tramitar solicitudes de QR. | Registro inmediato con validación de plantel existente y estatus inicial `PENDIENTE`. |
| **Gestión administrativa eficiente** | Permitir edición rápida por celda, búsqueda, paginación, borrado individual/masivo e importación/exportación Excel. | Operación sobre `planteles`, `solicitudes_qr` y `municipios` desde `ExcelDataGrid.vue`. |
| **Visibilidad analítica** | Ofrecer un dashboard ejecutivo con desglose por estatus QR, dependencia, municipio y rol solicitante. | Respuesta en tiempo real a *"¿Quién solicita mayormente códigos QR?"* vía `/api/dashboard/kpis`. |
| **Seguridad y continuidad** | Proteger operaciones administrativas mediante JWT y respaldar tablas automáticamente antes de importaciones masivas. | Respaldo previo automático en `backend/backups/` y limpieza programada en segundo plano. |

---

## 3. Usuarios y Roles

| Rol | Tipo de Acceso | Necesidades Principales |
| :--- | :--- | :--- |
| **Director / Enlace SEGEN / Supervisor / Representante** | Público (sin autenticación) | Buscar su plantel por Código DEA, cédula del director, nombre o municipio y registrar solicitudes de QR (`NUEVA_ASIGNACION`, `REPOSICION`, `CORRECCION`). |
| **Administrador de Zona Educativa** | Protegido (JWT Bearer) | Iniciar sesión en `/admin/login`, consultar KPIs en `/admin/dashboard`, aprobar/procesar solicitudes, editar celdas en `/admin/excel-grid`, descargar plantillas `.xlsx` y cargar actualizaciones masivas. |

---

## 4. Alcance Funcional (Implementado)

### 4.1 Portal Público de Solicitudes (`/`)
- Autocompletado y búsqueda de planteles por `codigo_dea`, `ci_contacto`, `nombres_contacto`, `plantel` o `municipio_nombre` (`GET /api/planteles/search`, `GET /api/planteles/dea/{query_key}`).
- Catálogo de municipios activos (`GET /api/planteles/municipios`).
- Envío de solicitudes QR (`POST /api/solicitudes`) con datos del solicitante (`solicitante_rol`, `solicitante_nombre`, `solicitante_ci`, `solicitante_telefono`, `solicitante_email`), `tipo_solicitud` y `motivo`.

### 4.2 Autenticación Administrativa (`/admin/login`)
- Inicio de sesión con usuario y contraseña (`POST /api/auth/login` usando `OAuth2PasswordRequestForm`).
- Emisión de token JWT (`HS256`, vigencia de 24 horas) almacenado en `localStorage` (`admin_token`) y verificado por `router.beforeEach`.

### 4.3 Dashboard Analítico (`/admin/dashboard`)
- Consumo de KPIs agregados (`GET /api/dashboard/kpis`):
  - Totales de planteles, `QR SEGEN`, `SIN QR ASIGNADO`, `REPONER QR` y solicitudes registradas.
  - Distribución por dependencia (`NACIONAL`, `ESTADAL`, `PRIVADA`).
  - Ranking de roles solicitantes (`ranking_roles` y `top_solicitante_rol`).
  - Desglose por estatus QR y resumen de los 6 municipios con mayor cantidad de planteles.
- Gestión de solicitudes (`GET /api/dashboard/solicitudes`, `PATCH /api/dashboard/solicitudes/{solicitud_id}/estatus`): al marcar una solicitud como `PROCESADO` o `COMPLETADO`, el plantel asociado se actualiza automáticamente a `estatus_qr = "QR SEGEN"`.

### 4.4 Data Grid Administrativo (`/admin/excel-grid`)
- Tabla interactiva basada en **AG Grid** (`ag-grid-vue3`) para `planteles`, `solicitudes_qr` y `municipios`.
- Búsqueda, paginación (`skip`/`limit`), edición directa por celda (`PATCH /api/admin/data/{table_name}/{row_id}`), creación (`POST`), eliminación individual (`DELETE`) y eliminación por lote (`POST /{table_name}/bulk-delete`).
- Descarga de plantilla oficial `.xlsx` (`GET /api/admin/data/download-template/{table_name}`).
- Carga masiva `.xlsx`/`.xlsm`/`.xls`/`.csv` (`POST /api/admin/data/{table_name}/upload-excel`) con respaldo automático previo (`backup_service.py`).
- Generación y visualización de códigos QR por plantel (`PlantelQrModal.vue`, `qrcode.vue`, `html2canvas`).

---

## 5. Requisitos No Funcionales

- **Rendimiento:** API FastAPI servida con Uvicorn; SPA Vue 3 compilada con Vite y servida por Nginx con proxy inverso hacia `/api/`.
- **Portabilidad:** Despliegue reproducible mediante `docker-compose.yml` (PostgreSQL 16 Alpine, Backend Python, Frontend Nginx) y soporte de desarrollo local con SQLite (`zona_educativa.db`).
- **Mantenibilidad:** Separación por capas en backend (`routers/`, `services/`, `models.py`, `schemas.py`) y modularidad en frontend (`views/`, `components/`, `composables/`, `stores/`).
- **Resiliencia:** Respaldo automático antes de cada importación Excel y servicio `cron_cleaner.py` iniciado en el evento `startup` de FastAPI.

