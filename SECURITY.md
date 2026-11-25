# Política y Auditoría de Seguridad — Zona Educativa

Este documento describe los controles de seguridad actualmente implementados en el repositorio, los hallazgos detectados durante la auditoría de código y el plan de endurecimiento requerido antes de un despliegue en producción.

---

## 1. Controles Actuales

| Área | Implementación Actual | Ubicación |
| :--- | :--- | :--- |
| **Autenticación** | OAuth2 Password Flow con JWT (`python-jose`, `SECRET_KEY`, `ALGORITHM` y `ACCESS_TOKEN_EXPIRE_MINUTES` vía variables de entorno; falla en arranque si falta `SECRET_KEY` en `ENVIRONMENT=production`) | `backend/app/routers/auth.py` |
| **Hashing de contraseñas** | `bcrypt.checkpw` / hashes bcrypt almacenados en `usuarios_admin.hashed_password` | `backend/app/routers/auth.py` |
| **CORS Restrictivo** | Orígenes permitidos desde `CORS_ORIGINS` (sin wildcard `*`), métodos y cabeceras explícitas | `backend/app/main.py` |
| **Protección de rutas FE** | Navigation Guard `router.beforeEach` verifica presencia de `admin_token` en `localStorage` | `frontend/src/router/index.js` |
| **Protección de rutas BE** | Dependencia `get_current_admin` aplicada a `/api/admin/data/*`, `/api/dashboard/*`, `GET /api/solicitudes` y `PATCH /api/solicitudes/{id}/estatus` | `backend/app/routers/admin_data.py`, `dashboard.py`, `solicitudes.py` |
| **Prevención de Mass Assignment** | Lista blanca `ALLOWED_COLUMNS` aplicada en `POST` y `PATCH` de tablas administrativas | `backend/app/routers/admin_data.py` |
| **Integridad en cargas masivas** | Validación de extensión (`.xlsx`, `.xlsm`, `.xls`, `.csv`) y respaldo automático previo | `backend/app/routers/admin_data.py`, `services/backup_service.py` |

---

## 2. Estado de Hallazgos de Auditoría

| Severidad | Hallazgo | Estado | Ubicación Real |
| :--- | :--- | :--- | :--- |
| **Crítica** | `SECRET_KEY` codificada en duro en código fuente | **Mitigado** (leída desde `os.getenv("SECRET_KEY")`; obligatoria en `ENVIRONMENT=production`) | `backend/app/routers/auth.py` |
| **Alta** | `GET /api/solicitudes` y `PATCH /api/solicitudes/{id}/estatus` sin autenticación | **Mitigado** (`Depends(get_current_admin)` añadido + header Bearer en `DashboardView.vue`) | `backend/app/routers/solicitudes.py`, `frontend/src/views/DashboardView.vue` |
| **Alta** | `CORSMiddleware` con `allow_origins=["*"]` | **Mitigado** (configurable vía `CORS_ORIGINS` con lista explícita de orígenes locales por defecto) | `backend/app/main.py` |
| **Alta** | *Mass Assignment* en `POST`/`PATCH` de `admin_data.py` | **Mitigado** (validación contra `ALLOWED_COLUMNS` por tabla) | `backend/app/routers/admin_data.py` |
| **Media** | `GET /api/dashboard/kpis` sin autenticación | **Mitigado** (`Depends(get_current_admin)` añadido + header Bearer en `stores/dashboard.js`) | `backend/app/routers/dashboard.py`, `frontend/src/stores/dashboard.js` |
| **Media** | Credenciales por defecto de PostgreSQL en `docker-compose.yml` | **Pendiente (Infra)** — Inyectar contraseñas fuertes desde secretos en producción | `docker-compose.yml:9,29` |
| **Media** | Token JWT almacenado en `localStorage` sin verificación de expiración en cliente | **Pendiente (Frontend)** — Migrar a cookies `HttpOnly` o validar expiración/interceptar `401` globalmente | `frontend/src/router/index.js:45` |

---

## 3. Plan de Endurecimiento para Producción

1. **Gestión de Secretos:**
   - Cargar `SECRET_KEY` desde `os.environ["SECRET_KEY"]` (fallar al iniciar si no existe) y generar una clave aleatoria de al menos 256 bits.
   - Eliminar contraseñas por defecto en `docker-compose.yml` para producción y usar secretos de entorno.
2. **Control de Acceso (RBAC / Auth):**
   - Proteger `GET /api/solicitudes`, `PATCH /api/solicitudes/{id}/estatus` y `GET /api/dashboard/kpis` con `Depends(get_current_admin)` (o unificar el flujo administrativo en `/api/dashboard/solicitudes`).
   - Implementar esquemas Pydantic estrictos y listas blancas de columnas editables en `admin_data.py`.
3. **CORS y Cabeceras HTTP:**
   - Restringir `allow_origins` al dominio real del frontend mediante variable de entorno `CORS_ORIGINS`.
   - Configurar HTTPS/TLS y cabeceras de seguridad (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`) en Nginx.
4. **Rate Limiting y Auditoría:**
   - Añadir límite de tasa (*rate limiting*) en `/api/auth/login` y `POST /api/solicitudes` para mitigar fuerza bruta y spam.
   - Registrar logs estructurados de auditoría para inicios de sesión, cambios de estatus y cargas masivas.

---

## 4. Reporte de Vulnerabilidades

Si detectas una vulnerabilidad de seguridad en este repositorio, repórtala de forma privada al equipo responsable antes de divulgarla públicamente, incluyendo pasos de reproducción e impacto estimado.

