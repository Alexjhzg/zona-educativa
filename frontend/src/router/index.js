import { createRouter, createWebHistory } from 'vue-router'
import SolicitudView from '../views/SolicitudView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'SolicitudPublica',
    component: SolicitudView,
    meta: { title: 'Solicitud de Código QR - Zona Educativa' }
  },
  {
    path: '/admin/login',
    name: 'LoginAdmin',
    component: LoginView,
    meta: { title: 'Acceso Administrativo - Zona Educativa' }
  },
  {
    path: '/admin/dashboard',
    name: 'DashboardAdmin',
    component: DashboardView,
    meta: { requiresAuth: true, title: 'Dashboard de Indicadores QR' }
  },
  {
    path: '/admin/excel-grid',
    name: 'ExcelDataGrid',
    component: () => import('../views/ExcelDataGrid.vue'),
    meta: { requiresAuth: true, title: 'Editar' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guarda de Navegación de Seguridad
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Zona Educativa'
  const token = localStorage.getItem('admin_token')

  if (to.meta.requiresAuth && !token) {
    next('/admin/login')
  } else {
    next()
  }
})

export default router
