---
name: vue3-developer
description: Desarrollador Frontend especialista en Vue 3 (Composition API <script setup>), Pinia, TailwindCSS, Vue Router 4 y Chart.js con separación de rutas públicas y protegidas.
---

# Skill: Vue 3 Frontend Developer

Este skill establece las reglas y arquitectura para la interfaz web interactiva con control de acceso por roles.

## Responsabilidades Principales:
1. **Control de Navegación y Rutas (Vue Router 4)**:
   - Ruta `/` (Pública): **Vista Solicitante (`SolicitudView.vue`)**. *Las personas externas solo ven el Formulario de Solicitud de QR sin menú ni acceso al Dashboard*.
   - Ruta `/admin/login` (Pública): **Vista Login (`LoginView.vue`)**.
   - Ruta `/admin/dashboard` (Protegida): **Vista Dashboard (`DashboardView.vue`)**. Guarda de navegación (`beforeEach`) para verificar token JWT de admin antes de conceder acceso.

2. **Formulario Público de Solicitud (`FormSolicitud.vue`)**:
   - Selector dinámico con autocompletado de plantel (búsqueda por DEA o Nombre).
   - Campos reactivos con feedback en tiempo real.
   - Confirmación Toast e instrucciones tras enviar solicitud.

3. **Dashboard Administrativo (`DashboardView.vue`)**:
   - Tarjetas de KPIs ejecutivos.
   - Indicador clave: *"¿Quién solicita mayormente cantidad de QR?"* (Ranking por Rol: Directores, Enlaces SEGEN, Supervisores).
   - Gráficos interactivos de Chart.js / ApexCharts.
   - Tabla interactiva con ordenamiento y filtros.
