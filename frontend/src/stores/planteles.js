import { defineStore } from 'pinia'
import axios from 'axios'

export const usePlantelesStore = defineStore('planteles', {
  state: () => ({
    searchResults: [],
    selectedPlantel: null,
    loadingSearch: false
  }),

  actions: {
    async buscarPlanteles(query) {
      if (!query || query.length < 2) {
        this.searchResults = []
        return
      }
      this.loadingSearch = true
      try {
        const response = await axios.get(`/api/planteles/search?q=${encodeURIComponent(query)}`)
        this.searchResults = response.data
      } catch (error) {
        console.error('Error buscando planteles:', error)
        this.searchResults = []
      } finally {
        this.loadingSearch = false
      }
    },

    async buscarPorCodigoDEA(codigoDEA) {
      if (!codigoDEA) return null
      this.loadingSearch = true
      try {
        const response = await axios.get(`/api/planteles/dea/${encodeURIComponent(codigoDEA.trim())}`)
        this.selectedPlantel = response.data
        return response.data
      } catch (error) {
        return null
      } finally {
        this.loadingSearch = false
      }
    }
  }
})
