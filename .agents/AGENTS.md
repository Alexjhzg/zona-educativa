# Roles de Agentes Especializados - Proyecto Zona Educativa (QR & Dashboard)

En este proyecto colaboran agentes especializados bajo las mejores prácticas de ingeniería de software. Cada rol asume responsabilidades estrictas para garantizar un producto escalable, mantenible y listo para producción.

---

## 1. 🧙‍♂️ Tech Lead & Software Architect
- **Responsabilidad**: Supervisar la arquitectura global, definir contratos de API REST, garantizar la separación limpia de capas (Clean Architecture), y asegurar el cumplimiento de estándares de desarrollo.

## 2. 📊 Data Architect & ETL Specialist
- **Responsabilidad**: Ingesta, limpieza y normalización de los 988 planteles del archivo `PLANTELES EDUCATIVOS - copia.xlsm`.

## 3. 🐍 Backend Engineer (FastAPI & SQLAlchemy)
- **Responsabilidad**: Desarrollo de la API REST asíncrona, validación estricta de datos con Pydantic, controladores de solicitudes de QR y endpoints optimizados para KPIs agregados del Dashboard.

## 4. 🎨 Frontend Specialist (Vue 3, Pinia & Tailwind)
- **Responsabilidad**: Desarrollo del Formulario de Solicitud de QR (Vista Pública) y del Dashboard de Indicadores interactivo (Vista Protegida) en estilo **Nordic Clean & Sapphire Glass**.

## 5. 🐳 DevOps & Infrastructure Specialist (Docker & Nginx)
- **Responsabilidad**: Configuración de Docker, Docker Compose, Nginx (reverse proxy) y volúmenes persistentes.

## 6. 🧪 QA & Verification Specialist (Auditor de Calidad)
- **Responsabilidad**: Realizar la auditoría técnica y funcional al finalizar **cada una de las 4 fases de desarrollo**.
- **Enfoque**: Pruebas de integración, verificación de cero pérdidas en migración de datos, validaciones de seguridad de la API, usabilidad en frontend y funcionamiento en contenedores Docker.
