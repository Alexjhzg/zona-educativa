<template>
  <AdminLayout active-section="dashboard">
    <template #header-left>
      <!-- Buscador Superior -->
      <div class="relative hidden md:block w-72">
        <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 shrink-0" />
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Buscar por DEA, Plantel o CI..."
          :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white placeholder-slate-400 focus:border-[#7bd0ff]' : 'bg-slate-100 border-slate-200 text-slate-900 placeholder-slate-400 focus:border-blue-900'"
          class="w-full border rounded-full py-1.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 transition-all"
        />
      </div>
    </template>

    <div class="space-y-8">
      <!-- Title Row -->
      <div class="flex flex-col sm:flex-row justify-between sm:items-end gap-4">
        <div>
          <h2 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-3xl font-black font-heading tracking-tight">Dashboard</h2>
          <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs mt-1 font-medium">Snapshot administrativo de los 988 planteles educativos de Monagas.</p>
        </div>
        <div class="flex items-center space-x-3">
          <router-link 
            to="/admin/excel-grid"
            :class="isDark ? 'bg-[#4edea3] text-[#003824] hover:bg-[#6ffbbe] shadow-[0_10px_20px_rgba(78,222,163,0.25)]' : 'bg-blue-900 text-white hover:bg-blue-950 shadow-md shadow-blue-900/20'"
            class="px-5 py-2.5 rounded-full font-extrabold text-xs flex items-center gap-2 transition-all cursor-pointer"
          >
            <Plus class="w-4 h-4" />
            <span>Editar</span>
          </router-link>
        </div>
      </div>

      <!-- KPI Row (4 Main Cards) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Card 1: Total Planteles en BD -->
        <div :class="isDark ? 'bg-white/5 border-white/10 hover:bg-white/10' : 'bg-white border-slate-200/80 shadow-md hover:border-purple-500/40'" class="backdrop-blur-xl rounded-2xl border p-6 relative overflow-hidden group transition-all">
          <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-purple-500 rounded-l-2xl"></div>
          <div class="flex justify-between items-start mb-3">
            <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs font-bold uppercase tracking-wider">Total Planteles BD</p>
            <div :class="isDark ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-100 text-purple-700'" class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0">
              <Building2 class="w-5 h-5 shrink-0" />
            </div>
          </div>
          <div class="flex items-baseline gap-2 mb-1">
            <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-4xl font-black font-mono">
              {{ kpisData.total_planteles || 988 }}
            </h3>
            <span class="text-xs font-bold text-purple-400">Instituciones</span>
          </div>
          <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-[11px] mt-2.5 font-medium flex items-center justify-between">
            <span>{{ kpisData.total_nacional || 650 }} Nac · {{ kpisData.total_estadal || 210 }} Est</span>
            <span class="text-emerald-500 font-bold">Base de Datos</span>
          </p>
        </div>

        <!-- Card 2: Cobertura Código QR -->
        <div :class="isDark ? 'bg-white/5 border-white/10 hover:bg-white/10' : 'bg-white border-slate-200/80 shadow-md hover:border-emerald-500/40'" class="backdrop-blur-xl rounded-2xl border p-6 relative overflow-hidden group transition-all">
          <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-[#4edea3] rounded-l-2xl"></div>
          <div class="flex justify-between items-start mb-3">
            <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs font-bold uppercase tracking-wider">Cobertura Código QR</p>
            <div :class="isDark ? 'bg-[#4edea3]/15 text-[#4edea3]' : 'bg-emerald-100 text-emerald-700'" class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0">
              <QrCode class="w-5 h-5 shrink-0" />
            </div>
          </div>
          <div class="flex items-baseline gap-2 mb-3">
            <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-4xl font-black font-mono">
              {{ (kpisData.total_planteles && kpisData.total_qr_segen ? ((kpisData.total_qr_segen / kpisData.total_planteles) * 100).toFixed(0) : 0) }}<span class="text-xl text-[#4edea3]">%</span>
            </h3>
          </div>
          <div :class="isDark ? 'bg-[#1c2b3c]' : 'bg-slate-100'" class="w-full rounded-full h-2 mt-2">
            <div 
              class="bg-[#4edea3] h-2 rounded-full transition-all duration-700 shadow-xs" 
              :style="{ width: (kpisData.total_planteles && kpisData.total_qr_segen ? ((kpisData.total_qr_segen / kpisData.total_planteles) * 100) : 0) + '%' }"
            ></div>
          </div>
          <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-[11px] mt-2.5 text-right font-medium">
            {{ kpisData.total_qr_segen || 0 }} de {{ kpisData.total_planteles || 0 }} planteles
          </p>
        </div>

        <!-- Card 3: Solicitudes Registradas -->
        <div :class="isDark ? 'bg-white/5 border-white/10 hover:bg-white/10' : 'bg-white border-slate-200/80 shadow-md hover:border-blue-500/40'" class="backdrop-blur-xl rounded-2xl border p-6 relative overflow-hidden group transition-all">
          <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-[#7bd0ff] rounded-l-2xl"></div>
          <div class="flex justify-between items-start mb-3">
            <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs font-bold uppercase tracking-wider">Solicitudes Registradas</p>
            <div :class="isDark ? 'bg-[#7bd0ff]/15 text-[#7bd0ff]' : 'bg-blue-100 text-blue-700'" class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0">
              <FileText class="w-5 h-5 shrink-0" />
            </div>
          </div>
          <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-4xl font-black font-mono">{{ solicitudes.length }}</h3>
          <p class="text-xs font-bold text-[#7bd0ff] mt-3 flex items-center gap-1">
            <svg class="w-4 h-4 text-[#7bd0ff]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
            </svg>
            <span>Activas en plataforma</span>
          </p>
        </div>

        <!-- Card 4: Cobertura Territorial -->
        <div :class="isDark ? 'bg-white/5 border-white/10 hover:bg-white/10' : 'bg-white border-slate-200/80 shadow-md hover:border-amber-500/40'" class="backdrop-blur-xl rounded-2xl border p-6 relative overflow-hidden group transition-all">
          <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-amber-400 rounded-l-2xl"></div>
          <div class="flex justify-between items-start mb-3">
            <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs font-bold uppercase tracking-wider">Cobertura Territorial</p>
            <div :class="isDark ? 'bg-amber-400/15 text-amber-400' : 'bg-amber-100 text-amber-700'" class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0">
              <MapPin class="w-5 h-5 shrink-0" />
            </div>
          </div>
          <div class="flex items-baseline gap-2">
            <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-4xl font-black font-mono">13<span :class="isDark ? 'text-slate-400' : 'text-slate-400'" class="text-xl">/13</span></h3>
          </div>
          <p class="text-xs font-bold text-amber-500 mt-3">100% Municipios Monagas</p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Section 1: Tabla de Solicitudes (2/3 width) -->
        <div class="lg:col-span-2 space-y-4">
          <div :class="isDark ? 'bg-white/5 border-white/10' : 'bg-white border-slate-200/80 shadow-sm'" class="flex justify-between items-center backdrop-blur-md p-5 rounded-t-2xl border border-b-0">
            <div>
              <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-lg font-black font-heading">Solicitudes de QR</h3>
              <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs mt-0.5">Gestión y actualización de estatus de planteles registrados.</p>
            </div>
            <div class="flex gap-2">
              <button 
                @click="loadData"
                :class="isDark ? 'bg-white/10 text-slate-200 hover:bg-white/20 border-white/10' : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border-slate-200'"
                class="px-3.5 py-1.5 rounded-lg transition-all text-xs font-bold border flex items-center gap-1.5 cursor-pointer"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                <span>Actualizar</span>
              </button>
            </div>
          </div>

          <div :class="isDark ? 'bg-white/5 border-white/10 shadow-xl' : 'bg-white border-slate-200/80 shadow-md'" class="backdrop-blur-xl rounded-b-2xl border border-t-0 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr :class="isDark ? 'border-white/10 text-slate-400 bg-[#122131]/60' : 'border-slate-200 text-slate-500 bg-slate-50'" class="border-b text-[11px] font-extrabold uppercase tracking-wider">
                    <th class="p-4 font-bold">Código DEA / Plantel</th>
                    <th class="p-4 font-bold">Municipio</th>
                    <th class="p-4 font-bold">Solicitante</th>
                    <th class="p-4 font-bold">Tipo Solicitud</th>
                    <th class="p-4 font-bold">Estatus</th>
                    <th class="p-4 font-bold text-right">Acción</th>
                  </tr>
                </thead>
                <tbody :class="isDark ? 'divide-white/5' : 'divide-slate-100'" class="text-xs font-medium divide-y">
                  <tr v-for="sol in filteredSolicitudes" :key="sol.id" :class="isDark ? 'hover:bg-white/5' : 'hover:bg-slate-50'" class="transition-colors group">
                    <td class="p-4">
                      <div class="font-extrabold text-[#7bd0ff]">{{ sol.plantel?.codigo_dea || sol.codigo_dea || '#MON-' + sol.id }}</div>
                      <div :class="isDark ? 'text-white' : 'text-slate-900'" class="font-bold text-xs truncate max-w-[200px]">{{ sol.plantel?.plantel || sol.nombre_plantel || 'Plantel Educativo' }}</div>
                    </td>
                    <td class="p-4 font-bold" :class="isDark ? 'text-amber-300' : 'text-amber-800'">
                      <div class="flex items-center gap-1">
                        <MapPin class="w-3.5 h-3.5 shrink-0 text-amber-500" />
                        <span>{{ sol.plantel?.municipio_nombre || sol.municipio_nombre || sol.plantel?.municipio || 'MATURIN' }}</span>
                      </div>
                    </td>
                    <td class="p-4">
                      <div :class="isDark ? 'text-white' : 'text-slate-900'" class="font-bold">{{ sol.solicitante_nombre || sol.nombre_solicitante || 'Solicitante' }}</div>
                      <div class="text-[10px] text-slate-400">CI: {{ sol.solicitante_ci || sol.cedula_solicitante || 'V-0000000' }}</div>
                    </td>
                    <td :class="isDark ? 'text-slate-300' : 'text-slate-700'" class="p-4 font-semibold">
                      {{ sol.tipo_solicitud || 'NUEVO_QR' }}
                    </td>
                    <td class="p-4">
                      <span 
                        :class="[
                          (sol.estatus_solicitud || sol.estatus) === 'PROCESADO' 
                            ? 'bg-[#4edea3]/15 text-[#4edea3] border-[#4edea3]/30' 
                            : 'bg-amber-400/15 text-amber-500 border-amber-400/30'
                        ]"
                        class="px-3 py-1 rounded-full text-[11px] font-extrabold border inline-block uppercase"
                      >
                        {{ sol.estatus_solicitud || sol.estatus || 'PENDIENTE' }}
                      </span>
                    </td>
                    <td class="p-4 text-right">
                      <button 
                        @click="toggleStatus(sol)"
                        :disabled="updatingStatusId === sol.id"
                        :class="isDark ? 'bg-[#4edea3] text-[#003824] hover:bg-[#6ffbbe]' : 'bg-blue-900 text-white hover:bg-blue-950'"
                        class="px-3 py-1.5 text-xs font-bold rounded-lg transition shadow-xs cursor-pointer"
                      >
                        {{ (sol.estatus_solicitud || sol.estatus) === 'PENDIENTE' ? 'Completar' : 'Reabrir' }}
                      </button>
                    </td>
                  </tr>

                  <tr v-if="filteredSolicitudes.length === 0">
                    <td colspan="5" class="p-8 text-center text-slate-400 text-xs">
                      No hay solicitudes encontradas para el filtro aplicado.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div :class="isDark ? 'bg-[#122131]/40 border-white/10 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'" class="p-4 border-t flex justify-between items-center text-xs">
              <span>Mostrando {{ filteredSolicitudes.length }} solicitudes</span>
            </div>
          </div>
        </div>

        <!-- Section 2: Upload Excel / Drag and Drop -->
        <div>
          <DragAndDropExcel @imported="loadData" />
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../stores/dashboard'
import { useAuthStore } from '../stores/auth'
import { useTheme } from '../composables/useTheme'
import { toast } from 'vue3-toastify'
import Swal from 'sweetalert2'
import axios from 'axios'
import AdminLayout from '../layouts/AdminLayout.vue'
import { 
  LayoutDashboard, 
  Table, 
  FileText, 
  QrCode, 
  LogOut, 
  Building2, 
  MapPin, 
  Search, 
  Sun, 
  Moon, 
  Plus, 
  RefreshCw, 
  CheckCircle2, 
  RotateCcw 
} from 'lucide-vue-next'

import DragAndDropExcel from '../components/admin/DragAndDropExcel.vue'

const dashboardStore = useDashboardStore()
const authStore = useAuthStore()
const router = useRouter()
const { isDark, toggleTheme } = useTheme()

const loading = ref(true)
const solicitudes = ref([])
const updatingStatusId = ref(null)

const searchQuery = ref('')

const kpisData = computed(() => {
  return dashboardStore.kpis || {
    total_planteles: 0,
    total_qr_segen: 0,
    total_sin_qr: 0,
    total_reponer_qr: 0,
    total_nacional: 0,
    total_estadal: 0,
    total_privada: 0,
    total_solicitudes_registradas: 0
  }
})

const userAdmin = computed(() => authStore.userAdmin || 'admin')

const filteredSolicitudes = computed(() => {
  let list = solicitudes.value
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(s => 
      (s.plantel?.codigo_dea && s.plantel.codigo_dea.toLowerCase().includes(q)) ||
      (s.plantel?.plantel && s.plantel.plantel.toLowerCase().includes(q)) ||
      (s.solicitante_nombre && s.solicitante_nombre.toLowerCase().includes(q)) ||
      (s.solicitante_ci && s.solicitante_ci.toLowerCase().includes(q))
    )
  }
  return list
})

async function loadData() {
  loading.value = true
  try {
    const token = authStore.token || localStorage.getItem('admin_token')
    await dashboardStore.fetchDashboardKPIs()
    const resp = await axios.get('/api/dashboard/solicitudes', {
      headers: { Authorization: `Bearer ${token}` }
    })
    solicitudes.value = resp.data || []
  } catch (err) {
    console.error('Error cargando datos del dashboard:', err)
  } finally {
    loading.value = false
  }
}

async function toggleStatus(sol) {
  updatingStatusId.value = sol.id
  const currentStatus = sol.estatus_solicitud || sol.estatus || 'PENDIENTE'
  const newStatus = currentStatus === 'PENDIENTE' ? 'PROCESADO' : 'PENDIENTE'
  try {
    await axios.patch(`/api/solicitudes/${sol.id}/estatus`, { estatus: newStatus, nuevo_estatus: newStatus })
    sol.estatus_solicitud = newStatus
    sol.estatus = newStatus
    toast.success(`Estatus cambiado a ${newStatus}`)
    await dashboardStore.fetchDashboardKPIs()
  } catch (err) {
    toast.error('Error al actualizar el estatus de la solicitud')
  } finally {
    updatingStatusId.value = null
  }
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
      popup: isDark.value ? 'bg-[#0d1c2d] text-white border border-white/10 rounded-3xl font-sans' : 'bg-white text-slate-900 rounded-3xl shadow-2xl font-sans'
    }
  })

  if (result.isConfirmed) {
    window.open('/solicitud', '_blank')
  }
}

function handleLogout() {
  authStore.logoutAdmin()
  router.push('/admin/login')
}

onMounted(() => {
  loadData()
})
</script>
