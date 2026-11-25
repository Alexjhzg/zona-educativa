import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    kpis: null,
    loadingKpis: false
  }),

  actions: {
    async fetchDashboardKPIs() {
      this.loadingKpis = true
      try {
        const authStore = useAuthStore()
        const token = authStore.token || localStorage.getItem('admin_token')
        const headers = token ? { Authorization: `Bearer ${token}` } : {}
        const response = await axios.get('/api/dashboard/kpis', { headers })
        this.kpis = response.data
      } catch (error) {
        console.error('Error al obtener KPIs:', error)
      } finally {
        this.loadingKpis = false
      }
    }
  }
})
