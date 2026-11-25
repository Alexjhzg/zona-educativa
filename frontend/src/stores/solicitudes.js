import { defineStore } from 'pinia'
import axios from 'axios'

export const useSolicitudesStore = defineStore('solicitudes', {
  actions: {
    async enviarSolicitudQR(payload) {
      const response = await axios.post('/api/solicitudes', payload)
      return response.data
    }
  }
})
