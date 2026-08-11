---
name: qa-engineer
description: Especialista en QA, auditoría de código, verificación de pruebas de integración y validación en las 4 fases de desarrollo.
---

# Skill: QA & Verification Specialist

Este skill dicta los protocolos de auditoría de calidad al finalizar cada fase del proyecto.

## Criterios de Aceptación por Fase:

### 🎯 Fase 1 (ETL, BD & Modelo de Datos):
- [ ] Verificar que los 988 planteles del XLSM hayan sido importados sin errores ni omitidos.
- [ ] Comprobar que los campos de `dependencia`, `municipio` y `estatus_qr` no tengan espacios en blanco ni inconsistencias de sintaxis.
- [ ] Validar claves primarias, foráneas e índices en SQLite/PostgreSQL.

### 🎯 Fase 2 (API Backend FastAPI):
- [ ] Verificar que `POST /api/solicitudes` valide correctamente la cédula, correo y seleccione planteles existentes.
- [ ] Comprobar que los endpoints de KPIs (`/api/dashboard/kpis`) devuelvan datos agregados exactos (`GROUP BY`).
- [ ] Confirmar que los endpoints protegidos devuelvan HTTP 401 si no hay token JWT válido.

### 🎯 Fase 3 (Frontend Formulario Público Vue 3):
- [ ] Verificar la experiencia de usuario (UX) en la vista pública `/` (Nordic Clean & Sapphire Glass).
- [ ] Confirmar que NO exista ningún enlace o fuga de datos hacia el Dashboard en la vista pública.
- [ ] Probar el autocompletado de planteles por código DEA y nombre.

### 🎯 Fase 4 (Frontend Dashboard Protegido & Docker):
- [ ] Probar la guarda de navegación de Vue Router (`/admin/dashboard` redirige a `/admin/login` si no está autenticado).
- [ ] Verificar el renderizado dinámico de los gráficos en Chart.js / ApexCharts para el indicador *"¿Quién solicita mayormente cantidad de QR?"*.
- [ ] Ejecutar `docker compose up --build` y certificar que la aplicación funcione al 100% de manera agnóstica.
