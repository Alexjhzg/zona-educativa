import { defineStore } from 'pinia'
import axios from 'axios'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    kpis: null,
    loadingKpis: false
  }),

  actions: {
    async fetchDashboardKPIs() {
      this.loadingKpis = true
      try {
        const response = await axios.get('/api/dashboard/kpis')
        this.kpis = response.data
      } catch (error) {
        console.error('Error al obtener KPIs:', error)
      } finally {
        this.loadingKpis = false
      }
    }
  }
})
