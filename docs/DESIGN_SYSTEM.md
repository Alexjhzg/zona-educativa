# Sistema de Diseño — Nordic Clean & Sapphire Glass

Este documento define los tokens reales, tipografía, paleta de colores y convenciones UI/UX implementadas en el frontend de **Zona Educativa** (`frontend/tailwind.config.js` y `frontend/src/style.css`).

---

## 1. Filosofía Visual

El lenguaje visual **Nordic Clean & Sapphire Glass** prioriza la legibilidad en jornadas prolongadas de análisis y edición tabular:
- Superficies claras con alto contraste tipográfico y soporte de modo oscuro mediante clase (`darkMode: 'class'` en TailwindCSS + composable `useTheme.js`).
- Paneles traslúcidos con desenfoque de fondo (*glassmorphism*) para tarjetas y modales.
- Iconografía uniforme basada en `lucide-vue-next`.

---

## 2. Paleta de Colores (Tokens TailwindCSS)

Definidos en [`frontend/tailwind.config.js`](../frontend/tailwind.config.js):

### 2.1 Escala Primaria (`sapphire`)
| Token | Hex | Uso Principal |
| :--- | :--- | :--- |
| `sapphire-50` | `#f0f5ff` | Fondos suaves de realce, badges e ítems activos |
| `sapphire-100` | `#e0ebff` | Bordes sutiles, hover de estados secundarios |
| `sapphire-500` | `#2563eb` | Acciones primarias, enlaces activos, foco |
| `sapphire-600` | `#1d4ed8` | Hover de botones primarios, énfasis |
| `sapphire-800` | `#1e3a8a` | Encabezados destacados, acentos profundos |
| `sapphire-900` | `#172554` | Contenedores oscuros y contraste alto |

### 2.2 Escala Neutra (`nordic`)
| Token | Hex | Uso Principal |
| :--- | :--- | :--- |
| `nordic-bg` | `#f8fafc` | Fondo general de la aplicación en modo claro |
| `nordic-card` | `#ffffff` | Superficie de tarjetas, formularios y modales |
| `nordic-text` | `#0f172a` | Texto principal de alta legibilidad |
| `nordic-muted` | `#64748b` | Texto secundario, etiquetas y metadatos |

---

## 3. Tipografía

Configurada en [`frontend/src/style.css`](../frontend/src/style.css):

| Rol | Familia Tipográfica | Aplicación |
| :--- | :--- | :--- |
| **Cuerpo / UI** | `'Inter', sans-serif` | `body`, formularios, tablas, etiquetas y botones |
| **Encabezados** | `'Plus Jakarta Sans', sans-serif` | `h1`–`h6` y clase utilitaria `.font-heading` |

---

## 4. Superficies y Glassmorphism

Clase utilitaria definida en `frontend/src/style.css`:

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
}
```

---

## 5. Componentes y Patrones UI

| Categoría | Librería / Implementación | Ubicación |
| :--- | :--- | :--- |
| **Layout Administrativo** | `AdminLayout.vue` | `frontend/src/layouts/AdminLayout.vue` |
| **Gráficos Analíticos** | `chart.js` + `vue-chartjs` | `frontend/src/components/DashboardKpis.vue` |
| **Data Grid** | `ag-grid-community` + `ag-grid-vue3` | `frontend/src/views/ExcelDataGrid.vue`, `frontend/src/components/grid/` |
| **Modales y Accesibilidad** | `@headlessui/vue` + `useModalKeyboard.js` | `frontend/src/components/grid/`, `frontend/src/composables/useModalKeyboard.js` |
| **Notificaciones y Confirmaciones** | `vue3-toastify` y `sweetalert2` | Flujos de guardado, eliminación y carga masiva |
| **Generación QR** | `qrcode` + `qrcode.vue` + `html2canvas` | `frontend/src/components/grid/PlantelQrModal.vue`, `useQrReport.js` |

---

## 6. Reglas de UX y Accesibilidad

1. **Separación de flujos:** El portal público (`/`) no expone navegación administrativa; las rutas `/admin/*` utilizan `AdminLayout.vue`.
2. **Retroalimentación inmediata:** Toda mutación asíncrona (envío de solicitud, edición de celda, carga Excel, borrado) debe mostrar estado de carga y notificación clara de éxito o error.
3. **Soporte de teclado:** Los modales administrativos deben cerrar con `Escape` y respetar el foco mediante `useModalKeyboard.js`.
4. **Responsividad:** Todas las vistas deben adaptarse a pantallas de escritorio y móviles usando utilidades responsive de TailwindCSS (`sm:`, `md:`, `lg:`).

