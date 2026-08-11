import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import router from './router'
import App from './App.vue'
import './style.css'

// Configurar URL del Backend (Render API o Local)
if (import.meta.env.VITE_API_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_URL
}

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Vue3Toastify, {
  autoClose: 3000,
  position: 'top-right',
  theme: 'colored'
})

app.mount('#app')
