# Guía de Estilo de Código — Zona Educativa

Este documento define las convenciones de formato, linting y buenas prácticas configuradas en el proyecto.

---

## 1. Reglas Generales (`.editorconfig`)

- **Codificación:** `UTF-8`
- **Saltos de línea:** `LF`
- **Espacios al final de línea:** Eliminados automáticamente (excepto en `.md`)
- **Línea final:** Obligatoria en todos los archivos
- **Indentación:**
  - Python (`.py`): 4 espacios
  - JS / Vue / JSON / CSS / YAML / HTML: 2 espacios

---

## 2. Backend (Python / FastAPI)

Configurado en [`backend/pyproject.toml`](../backend/pyproject.toml) con **Ruff** y **pytest**.

- **Longitud máxima de línea:** 100 caracteres
- **Reglas activas en Ruff:** `E`, `F`, `W`, `I` (orden de imports), `B` (bugbear), `UP` (pyupgrade)
- **Comandos de verificación:**
  ```bash
  cd backend
  ./venv/bin/ruff check app tests
  ./venv/bin/ruff format --check app tests
  ./venv/bin/pytest
  ```
- **Convenciones:**
  - Tipado estricto en parámetros de endpoints, esquemas Pydantic v2 y funciones auxiliares.
  - Separación de responsabilidades: `routers/` (HTTP), `services/` (lógica de negocio/soporte), `models.py` (ORM), `schemas.py` (DTOs).

---

## 3. Frontend (Vue 3 / Vite / TailwindCSS)

Configurado en `frontend/eslint.config.js`, `frontend/.prettierrc.json` y `frontend/package.json`.

- **Herramientas:** ESLint 9 (Flat Config + `eslint-plugin-vue`) y Prettier.
- **Comandos de verificación:**
  ```bash
  cd frontend
  npm run lint
  npm run format:check
  npm run build
  ```
- **Convenciones:**
  - Usar Vue 3 Composition API con `<script setup>`.
  - Componentes en `PascalCase` (`PlantelQrModal.vue`), composables en `camelCase` con prefijo `use` (`useGridData.js`), stores Pinia en `camelCase`.
  - Mantener estilos consistentes con los tokens `sapphire-*` y `nordic-*` de TailwindCSS.

