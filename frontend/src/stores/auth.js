import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    userAdmin: localStorage.getItem('admin_user') || ''
  }),

  actions: {
    async loginAdmin(username, password) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)

      const response = await axios.post('/api/auth/login', formData)
      this.token = response.data.access_token
      this.userAdmin = response.data.username
      localStorage.setItem('admin_token', this.token)
      localStorage.setItem('admin_user', this.userAdmin)
      return true
    },

    logoutAdmin() {
      this.token = ''
      this.userAdmin = ''
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
    }
  }
})
