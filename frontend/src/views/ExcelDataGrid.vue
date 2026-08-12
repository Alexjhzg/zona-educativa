<template>
  <AdminLayout active-section="editar">
    <template #header-left>
      <div>
        <p :class="isDark ? 'text-white' : 'text-slate-900'" class="text-sm font-extrabold leading-tight">Editar</p>
        <p class="text-xs text-slate-400 font-medium">{{ totalRows }} registros · Monagas</p>
      </div>
    </template>

    <div class="space-y-5">
      <!-- Selector de Pestañas de Tablas -->
      <GridTableTabs
        :active-table="activeTable"
        :total-rows="totalRows"
        @switch-table="switchTable"
      />

      <!-- Barra de Herramientas -->
      <GridToolbar
        v-model:search-query="searchQuery"
        :selected-count="selectedRowsList.length"
        :can-undo="undoStack.length > 0"
        :can-redo="redoStack.length > 0"
        @export-excel="exportExcelWithExcelJS"
        @open-add-modal="showAddModal = true"
        @open-dropzone="showDropzoneModal = true"
        @delete-selected="deleteSelectedRows"
        @undo="undo"
        @redo="redo"
      />

      <!-- Motor AG-Grid -->
      <div class="relative">
        <div v-if="loading" class="py-20 text-center font-medium text-sm bg-white/5 rounded-2xl border border-white/10 text-slate-400">
          <div class="flex flex-col items-center gap-4">
            <div class="w-10 h-10 border-2 border-[#4edea3]/30 border-t-[#4edea3] rounded-full animate-spin"></div>
            <span>Cargando registros...</span>
          </div>
        </div>

        <AgGridTable
          v-else
          ref="agGridRef"
          :row-data="rows"
          :column-defs="columnDefs"
          :quick-filter-text="searchQuery"
          @cell-value-changed="handleCellValueChanged"
          @delete-rows="deleteRows"
          @selection-changed="handleSelectionChanged"
          @show-qr-modal="openQrModalForPlantel"
        />
      </div>

      <!-- Modal de Agregar Nueva Fila -->
      <GridAddRowModal
        v-if="showAddModal"
        :active-table="activeTable"
        :columns="modalColumns"
        :planteles-list="rows"
        v-model:new-row-form="newRowForm"
        :saving-new-row="savingNewRow"
        @close="showAddModal = false"
        @save-new-row="saveNewRow"
      />

      <!-- Overlay Global Drag & Drop -->
      <div
        v-if="isScreenDragging"
        class="fixed inset-0 z-50 bg-blue-900/80 backdrop-blur-md flex flex-col items-center justify-center p-6 text-white border-4 border-dashed border-white/60 animate-fade-in pointer-events-none"
      >
        <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mb-6 shadow-2xl animate-bounce">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
        </div>
        <h2 class="text-2xl font-extrabold text-center">
          Suelta tu archivo Excel o CSV en cualquier parte de la pantalla
        </h2>
        <p class="text-sm font-medium text-blue-100 mt-2 text-center">
          Se generará un respaldo automático previo y se actualizarán los datos de {{ activeTable.toUpperCase() }}
        </p>
      </div>

      <!-- Modal Drag & Drop Excel/CSV -->
      <GridDropzoneModal
        :is-open="showDropzoneModal"
        :table-name="activeTable"
        :initial-file="droppedFile"
        @close="closeDropzoneModal"
        @upload-success="loadTableData"
      />

      <!-- Modal de Visualización de Código QR (Nativo) -->
      <PlantelQrModal
        :is-open="showQrModal"
        :plantel="selectedPlantelForQr"
        :plantel-list="rows"
        @close="showQrModal = false"
      />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCatalogosStore } from '../stores/catalogos'
import { useTheme } from '../composables/useTheme'
import { useColumnDefs } from '../composables/useColumnDefs'
import { useGridData } from '../composables/useGridData'
import { toast } from 'vue3-toastify'
import Swal from 'sweetalert2'
import ExcelJS from 'exceljs'
import AdminLayout from '../layouts/AdminLayout.vue'

import GridTableTabs from '../components/grid/GridTableTabs.vue'
import GridToolbar from '../components/grid/GridToolbar.vue'
import GridAddRowModal from '../components/grid/GridAddRowModal.vue'
import AgGridTable from '../components/grid/AgGridTable.vue'
import GridDropzoneModal from '../components/grid/GridDropzoneModal.vue'
import PlantelQrModal from '../components/grid/PlantelQrModal.vue'

const authStore = useAuthStore()
const catalogosStore = useCatalogosStore()
const router = useRouter()

// Estado del Modal de QR
const showQrModal = ref(false)
const selectedPlantelForQr = ref(null)

function openQrModalForPlantel(plantel) {
  selectedPlantelForQr.value = plantel
  showQrModal.value = true
}
const { isDark } = useTheme()

// Estado de tabla activa
const activeTable = ref('planteles')
const searchQuery = ref('')
const agGridRef = ref(null)

// Composable de Datos
const {
  rows,
  totalRows,
  loading,
  selectedRowsList,
  undoStack,
  redoStack,
  loadTableData,
  handleCellValueChanged,
  saveNewRow: saveNewRowData,
  deleteRows,
  deleteSelectedRows,
  undo,
  redo,
  handleSelectionChanged
} = useGridData(activeTable)

// Modales
const showAddModal = ref(false)
const showDropzoneModal = ref(false)
const savingNewRow = ref(false)
const newRowForm = reactive({})

// Drag & Drop global
const isScreenDragging = ref(false)
const droppedFile = ref(null)
let dragCounter = 0

// Usuario admin del store
const userAdmin = computed(() => authStore.userAdmin || 'admin')

// ==================== DEFINICIÓN DE COLUMNAS ====================
const { columnDefs, modalColumns } = useColumnDefs(activeTable)

// ==================== SAVE NEW ROW ====================
async function saveNewRow() {
  savingNewRow.value = true
  await saveNewRowData(newRowForm, () => {
    showAddModal.value = false
    Object.keys(newRowForm).forEach(k => delete newRowForm[k])
  })
  savingNewRow.value = false
}

// ==================== DRAG & DROP HANDLERS ====================
function handleWindowDragEnter(e) {
  e.preventDefault()
  dragCounter++
  if (e.dataTransfer && e.dataTransfer.types.includes('Files')) {
    isScreenDragging.value = true
  }
}
function handleWindowDragOver(e) {
  e.preventDefault()
  if (e.dataTransfer && e.dataTransfer.types.includes('Files')) {
    isScreenDragging.value = true
  }
}
function handleWindowDragLeave(e) {
  e.preventDefault()
  dragCounter--
  if (dragCounter <= 0) {
    dragCounter = 0
    isScreenDragging.value = false
  }
}
function handleWindowDrop(e) {
  e.preventDefault()
  dragCounter = 0
  isScreenDragging.value = false
  if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    droppedFile.value = e.dataTransfer.files[0]
    showDropzoneModal.value = true
  }
}
function closeDropzoneModal() {
  showDropzoneModal.value = false
  droppedFile.value = null
}

function handleGlobalKeyDown(e) {
  const activeTag = document.activeElement?.tagName
  if (['INPUT', 'TEXTAREA'].includes(activeTag)) return
  if (e.ctrlKey || e.metaKey) {
    const key = e.key.toLowerCase()
    if (key === 'z') {
      e.preventDefault()
      if (e.shiftKey) { redo() } else { undo() }
    } else if (key === 'y') {
      e.preventDefault()
      redo()
    }
  }
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  catalogosStore.cargarCatalogos()
  await loadTableData()
  window.addEventListener('dragenter', handleWindowDragEnter)
  window.addEventListener('dragover', handleWindowDragOver)
  window.addEventListener('dragleave', handleWindowDragLeave)
  window.addEventListener('drop', handleWindowDrop)
  window.addEventListener('keydown', handleGlobalKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('dragenter', handleWindowDragEnter)
  window.removeEventListener('dragover', handleWindowDragOver)
  window.removeEventListener('dragleave', handleWindowDragLeave)
  window.removeEventListener('drop', handleWindowDrop)
  window.removeEventListener('keydown', handleGlobalKeyDown)
})

// ==================== DATA LOADING ====================
async function switchTable(tableName) {
  activeTable.value = tableName
  searchQuery.value = ''
  Object.keys(newRowForm).forEach(k => delete newRowForm[k])
  await loadTableData()
}

// ==================== EXPORT EXCEL ====================
async function exportExcelWithExcelJS() {
  if (!rows.value || rows.value.length === 0) {
    toast.warning('No hay filas disponibles para exportar.')
    return
  }
  try {
    const workbook = new ExcelJS.Workbook()
    const worksheet = workbook.addWorksheet(activeTable.value.toUpperCase())
    const headers = columnDefs.value.map(c => ({
      header: c.headerName.toUpperCase(),
      key: c.field,
      width: Math.max(c.headerName.length + 5, 18)
    }))
    worksheet.columns = headers
    const headerRow = worksheet.getRow(1)
    headerRow.height = 24
    headerRow.eachCell((cell) => {
      cell.font = { name: 'Calibri', size: 11, bold: true, color: { argb: 'FF000000' } }
      cell.alignment = { vertical: 'middle', horizontal: 'left' }
    })
    rows.value.forEach(row => { worksheet.addRow(row) })
    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `MATRIZ_${activeTable.value.toUpperCase()}_${new Date().toISOString().slice(0, 10)}.xlsx`
    document.body.appendChild(a)
    a.click()
    a.remove()
    toast.success('Archivo Excel (.xlsx) generado y descargado exitosamente.')
  } catch (err) {
    console.error(err)
    toast.error('Error al exportar el archivo Excel.')
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
</script>
