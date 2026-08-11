<template>
  <div class="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-3xl shadow-xl shadow-slate-200/60 border border-slate-100 p-8">
      <div class="text-center mb-8">
        <div class="w-14 h-14 bg-blue-900 text-white rounded-2xl flex items-center justify-center font-bold text-2xl mx-auto mb-3 shadow-lg shadow-blue-900/20">
          ZE
        </div>
        <h2 class="text-2xl font-extrabold text-slate-900 font-heading">Acceso Administrativo</h2>
        <p class="text-xs text-slate-500 font-medium mt-1">
          Dashboard de Indicadores y Gestión de QR
        </p>
      </div>

      <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 text-xs font-semibold rounded-xl p-3 mb-4">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Usuario</label>
          <input
            v-model="username"
            type="text"
            placeholder="Ingresa tu usuario (ej. admin)"
            class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-800/30"
            required
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Contraseña</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-800/30"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3.5 bg-blue-900 hover:bg-blue-950 text-white font-bold text-sm rounded-xl transition shadow-lg shadow-blue-900/20 cursor-pointer"
        >
          <span v-if="loading">Iniciando Sesión...</span>
          <span v-else>Ingresar al Dashboard</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <router-link to="/" class="text-xs text-slate-400 hover:text-slate-600 font-medium">
          ← Volver al Formulario Público
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const store = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''
  try {
    await store.loginAdmin(username.value, password.value)
    router.push('/admin/dashboard')
  } catch (err) {
    errorMessage.value = 'Usuario o contraseña incorrectos. (Demo: admin / admin123)'
  } finally {
    loading.value = false
  }
}
</script>
