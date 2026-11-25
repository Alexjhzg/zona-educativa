import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'
import { useDashboardStore } from './dashboard'

export const useAdminStore = defineStore('admin', {
  actions: {
    async importarExcel(file) {
      const authStore = useAuthStore()
      const dashboardStore = useDashboardStore()

      const formData = new FormData()
      formData.append('file', file)

      const headers = {
        'Content-Type': 'multipart/form-data'
      }

      if (authStore.token) {
        headers['Authorization'] = `Bearer ${authStore.token}`
      }

      const response = await axios.post('/api/admin/data/import-excel', formData, { headers })
      // Refrescar KPIs de forma asíncrona tras actualizar la BD
      await dashboardStore.fetchDashboardKPIs()
      return response.data
    }
  }
})
