import { defineStore } from 'pinia'
import axios from 'axios'
import {
  MUNICIPIOS_MONAGAS,
  DEPENDENCIAS,
  ESTATUS_QR_LIST,
  ROLES_LIST,
  TIPO_SOLICITUD_LIST,
  ESTATUS_SOLICITUD_LIST
} from '../constants/gridOptions'

export const useCatalogosStore = defineStore('catalogos', {
  state: () => ({
    municipios: [...MUNICIPIOS_MONAGAS],
    dependencias: [...DEPENDENCIAS],
    estatusQrList: [...ESTATUS_QR_LIST],
    rolesList: [...ROLES_LIST],
    tiposSolicitudList: [...TIPO_SOLICITUD_LIST],
    estatusSolicitudList: [...ESTATUS_SOLICITUD_LIST],
    loadingCatalogos: false,
    loadedFromDb: false
  }),

  actions: {
    normalizeMunicipioName(val) {
      if (!val) return 'MATURÍN'
      const clean = String(val).trim().toUpperCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace("PUNERES", "PUNCERES")
      
      for (const m of this.municipios) {
        const cleanM = m.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        if (clean === cleanM) {
          return m
        }
      }
      return String(val).toUpperCase()
    },

    async cargarCatalogos() {
      if (this.loadingCatalogos) return
      this.loadingCatalogos = true
      try {
        const resp = await axios.get('/api/planteles/municipios')
        if (resp.data && Array.isArray(resp.data) && resp.data.length > 0) {
          const rawDbList = resp.data
          const mergedList = []
          
          rawDbList.forEach(raw => {
            const normalized = this.normalizeMunicipioName(raw)
            if (!mergedList.includes(normalized)) {
              mergedList.push(normalized)
            }
          })

          MUNICIPIOS_MONAGAS.forEach(m => {
            if (!mergedList.includes(m)) {
              mergedList.push(m)
            }
          })

          this.municipios = mergedList
          this.loadedFromDb = true
        }
      } catch (err) {
        console.info('Usando catálogo estático fallback de municipios.')
      } finally {
        this.loadingCatalogos = false
      }
    }
  }
})
