<template>
  <div
    :class="isDark ? 'bg-[#051424] text-[#d4e4fa]' : 'bg-[#F8FAFC] text-[#0F172A]'"
    class="min-h-screen font-sans antialiased overflow-x-hidden transition-colors duration-300"
  >
    <!-- Overlay Móvil para cerrar el menú al hacer tap afuera -->
    <div
      v-if="isMobileOpen"
      @click="isMobileOpen = false"
      class="fixed inset-0 z-40 bg-black/60 backdrop-blur-xs md:hidden transition-opacity"
    ></div>

    <!-- SideNavBar (Desktop Fijo + Mobile Drawer) -->
    <nav
      :class="[
        isDark ? 'bg-[#051424]/95 border-white/10 shadow-[0_20px_40px_rgba(0,0,0,0.4)]' : 'bg-white border-slate-200/80 shadow-lg',
        isMobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      ]"
      class="w-[260px] h-screen fixed left-0 top-0 border-r flex flex-col py-8 px-6 z-50 transition-transform duration-300 ease-in-out"
    >
      <!-- Brand Header + Close button on mobile -->
      <div class="mb-8 flex items-center justify-between px-2">
        <div class="flex items-center gap-3">
          <div class="w-11 h-11 rounded-2xl border border-white/20 bg-blue-950 shrink-0 flex items-center justify-center text-white font-black text-base shadow-md shadow-blue-900/30">
            ZE
          </div>
          <div>
            <h1 :class="isDark ? 'text-white' : 'text-slate-900'" class="font-extrabold text-lg leading-tight tracking-tight">Zona Educativa</h1>
            <p class="text-[11px] text-slate-400 font-semibold tracking-wider uppercase">Monagas Admin</p>
          </div>
        </div>

        <button
          @click="isMobileOpen = false"
          class="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Navigation Links -->
      <div class="flex-1 overflow-y-auto space-y-2">
        <!-- Dashboard -->
        <component
          :is="activeSection === 'dashboard' ? 'div' : 'router-link'"
          to="/admin/dashboard"
          @click="isMobileOpen = false"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl transition-all cursor-pointer',
            activeSection === 'dashboard'
              ? (isDark ? 'text-[#4edea3] border-[#4edea3] bg-white/5 font-bold border-r-2 shadow-xs' : 'text-blue-900 font-black border-blue-900 bg-blue-50/80 border-r-2 shadow-xs')
              : (isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white font-medium' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-medium')
          ]"
        >
          <LayoutDashboard
            :class="activeSection === 'dashboard'
              ? (isDark ? 'text-[#4edea3]' : 'text-blue-900')
              : 'text-slate-400'"
            class="w-5 h-5 shrink-0"
          />
          <span>Dashboard</span>
        </component>

        <!-- Editar -->
        <component
          :is="activeSection === 'editar' ? 'div' : 'router-link'"
          to="/admin/excel-grid"
          @click="isMobileOpen = false"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl transition-all cursor-pointer',
            activeSection === 'editar'
              ? (isDark ? 'text-[#4edea3] border-[#4edea3] bg-white/5 font-bold border-r-2 shadow-xs' : 'text-blue-900 font-black border-blue-900 bg-blue-50/80 border-r-2 shadow-xs')
              : (isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white font-medium' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 font-medium')
          ]"
        >
          <Table
            :class="activeSection === 'editar'
              ? (isDark ? 'text-[#4edea3]' : 'text-blue-900')
              : 'text-slate-400'"
            class="w-5 h-5 shrink-0"
          />
          <span>Editar</span>
        </component>

        <!-- Formulario QR -->
        <button
          @click="confirmFormularioQR"
          :class="isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all cursor-pointer"
        >
          <FileText class="w-5 h-5 text-slate-400 shrink-0" />
          <span>Formulario QR</span>
        </button>
      </div>

      <!-- Logout Bottom -->
      <div :class="isDark ? 'border-white/10' : 'border-slate-200'" class="pt-4 border-t">
        <button
          @click="handleLogout"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-500 hover:bg-red-500/10 font-bold transition-all text-xs cursor-pointer"
        >
          <LogOut class="w-4 h-4 text-red-500 shrink-0" />
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </nav>

    <!-- TopNavBar Fijo -->
    <header
      :class="isDark ? 'bg-[#051424]/90 border-white/10' : 'bg-white/90 border-slate-200/80 shadow-xs'"
      class="fixed top-0 right-0 w-full md:w-[calc(100%-260px)] h-16 backdrop-blur-md border-b flex justify-between items-center px-4 md:px-10 z-40 transition-colors duration-300"
    >
      <!-- Lado Izquierdo: Botón Hamburguesa Móvil + Slot -->
      <div class="flex items-center gap-3">
        <button
          @click="isMobileOpen = !isMobileOpen"
          :class="isDark ? 'bg-white/10 text-white hover:bg-white/20 border-white/15' : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border-slate-200'"
          class="md:hidden p-2 rounded-xl border transition-all cursor-pointer flex items-center justify-center"
          title="Abrir Menú"
        >
          <Menu class="w-5 h-5 shrink-0" />
        </button>

        <slot name="header-left" />
      </div>

      <!-- Lado Derecho: tema + badge + slot opcional -->
      <div class="flex items-center gap-3 text-xs font-bold">
        <slot name="header-right" />

        <!-- Toggle Tema -->
        <button
          @click="toggleTheme"
          :class="isDark ? 'bg-white/10 border-white/15 text-amber-300 hover:bg-white/20' : 'bg-slate-100 border-slate-200 text-slate-700 hover:bg-slate-200'"
          class="p-2 rounded-full border transition-all cursor-pointer flex items-center justify-center shadow-xs"
          :title="isDark ? 'Cambiar a Modo Claro' : 'Cambiar a Modo Oscuro'"
        >
          <Sun v-if="isDark" class="w-4 h-4 text-amber-300 shrink-0" />
          <Moon v-else class="w-4 h-4 text-slate-700 shrink-0" />
        </button>

        <!-- Badge Admin -->
        <div
          :class="isDark ? 'bg-white/5 border-white/10 text-white' : 'bg-slate-100 border-slate-200 text-slate-800'"
          class="flex items-center space-x-2 border px-3.5 py-1.5 rounded-full"
        >
          <span class="w-2 h-2 rounded-full bg-[#4edea3] animate-pulse"></span>
          <span>{{ userAdmin }}</span>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="pt-24 pb-12 px-4 md:px-8 md:ml-[260px] min-h-screen">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { LayoutDashboard, Table, FileText, LogOut, Sun, Moon, Menu, X } from 'lucide-vue-next'
import { useTheme } from '../composables/useTheme'
import { useAuthStore } from '../stores/auth'
import Swal from 'sweetalert2'

const props = defineProps({
  /** Sección activa: 'dashboard' | 'editar' */
  activeSection: {
    type: String,
    default: ''
  }
})

const isMobileOpen = ref(false)
const { isDark, toggleTheme } = useTheme()
const authStore = useAuthStore()
const router = useRouter()

const userAdmin = computed(() => authStore.userAdmin || 'admin')

function handleLogout() {
  authStore.logoutAdmin()
  router.push('/admin/login')
}

async function confirmFormularioQR() {
  const result = await Swal.fire({
    title: '¿Salir del Módulo Administrador?',
    text: 'Estás a punto de ingresar al Formulario Público de Solicitud de Código QR.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#1d4ed8',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Sí, ir al Formulario',
    cancelButtonText: 'Cancelar',
    customClass: {
      popup: isDark.value
        ? 'bg-[#0d1c2d] text-white border border-white/10 rounded-3xl font-sans'
        : 'bg-white text-slate-900 rounded-3xl shadow-2xl font-sans'
    }
  })
  if (result.isConfirmed) {
    window.open('/solicitud', '_blank')
  }
}
</script>
