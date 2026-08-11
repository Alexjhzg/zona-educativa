<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
    <div class="bg-white rounded-3xl shadow-2xl border border-slate-200 w-full max-w-xl p-6 relative overflow-hidden">
      <!-- Encabezado del Modal -->
      <div class="flex items-center justify-between border-b border-slate-100 pb-4 mb-5">
        <div class="flex items-center space-x-3">
          <div class="p-2.5 bg-blue-50 text-blue-900 rounded-2xl">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </div>
          <div>
            <h3 class="text-base font-extrabold text-slate-900">Importar Archivo Excel / CSV</h3>
            <p class="text-xs text-slate-500 font-medium">Actualización masiva con respaldo automático congelado</p>
          </div>
        </div>
        <button @click="close" class="text-slate-400 hover:text-slate-600 font-bold p-1 rounded-lg transition cursor-pointer">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Zona de Arrastre Drag & Drop -->
      <div
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
        :class="[
          'border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition flex flex-col items-center justify-center space-y-3',
          isDragging ? 'border-blue-600 bg-blue-50/70 scale-[1.01]' : 'border-slate-300 hover:border-blue-900/50 bg-slate-50/50 hover:bg-slate-50'
        ]"
      >
        <input
          type="file"
          ref="fileInputRef"
          @change="handleFileSelect"
          accept=".xlsx,.xlsm,.xls,.csv"
          class="hidden"
        />

        <div class="w-12 h-12 rounded-full bg-blue-100 text-blue-900 flex items-center justify-center shadow-xs">
          <svg class="w-6 h-6 text-blue-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>

        <div>
          <p class="text-xs font-bold text-slate-800">
            Arrastra y suelta tu archivo Excel o CSV aquí
          </p>
          <p class="text-[11px] text-slate-500 mt-1">
            Formatos soportados: <span class="font-bold text-blue-900">.xlsx, .xlsm, .xls, .csv</span>
          </p>
        </div>

        <div class="flex items-center space-x-2 pt-1">
          <button type="button" class="px-4 py-2 bg-white border border-slate-300 text-slate-700 text-xs font-bold rounded-xl shadow-xs hover:bg-slate-50 transition cursor-pointer">
            Examinar Archivo Local
          </button>
          <button type="button" @click.stop="downloadOfficialTemplate" class="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-900 border border-blue-200 text-xs font-bold rounded-xl transition cursor-pointer flex items-center space-x-1.5">
            <svg class="w-4 h-4 text-blue-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            <span>Descargar Plantilla Oficial</span>
          </button>
        </div>
      </div>

      <!-- Archivo Seleccionado y Progreso -->
      <div v-if="selectedFile" class="mt-4 p-3.5 bg-blue-50/80 border border-blue-200 rounded-2xl flex items-center justify-between text-xs">
        <div class="flex items-center space-x-2 truncate">
          <svg class="w-4 h-4 text-blue-900 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/>
          </svg>
          <span class="font-bold text-blue-900 truncate">{{ selectedFile.name }}</span>
          <span class="text-slate-500 shrink-0">({{ (selectedFile.size / 1024).toFixed(1) }} KB)</span>
        </div>
        <button v-if="!uploading" @click.stop="selectedFile = null" class="text-slate-400 hover:text-red-600 font-bold px-2 cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Banner de Resumen de Respuesta / Respaldo -->
      <div v-if="resultSummary" class="mt-4 p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs space-y-2 animate-fade-in">
        <div class="flex items-center space-x-2 text-emerald-900 font-bold">
          <svg class="w-4 h-4 text-emerald-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <span>{{ resultSummary.message }}</span>
        </div>
        <div v-if="resultSummary.backup_file" class="flex items-center space-x-2 text-slate-600 text-[11px]">
          <svg class="w-4 h-4 text-slate-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
          </svg>
          <span><span class="font-semibold">Respaldo generado:</span> <code class="bg-emerald-100 text-emerald-900 px-1.5 py-0.5 rounded font-mono">{{ resultSummary.backup_file }}</code> (Retención de 7 días).</span>
        </div>
        <div v-if="resultSummary.detalles" class="text-slate-600 text-[11px] font-medium pt-1 border-t border-emerald-200/60 flex space-x-4">
          <span>Filas Procesadas: <b>{{ resultSummary.detalles.total_filas }}</b></span>
          <span>Actualizadas: <b>{{ resultSummary.detalles.actualizados }}</b></span>
          <span>Creadas: <b>{{ resultSummary.detalles.creados }}</b></span>
        </div>
      </div>

      <!-- Banner de Error -->
      <div v-if="errorMessage" class="mt-4 p-3.5 bg-red-50 border border-red-200 rounded-2xl text-xs text-red-700 font-bold flex items-center space-x-2">
        <svg class="w-4 h-4 text-red-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- Acciones del Modal -->
      <div class="mt-6 flex items-center justify-end space-x-3 border-t border-slate-100 pt-4">
        <button
          @click="close"
          class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
        >
          {{ resultSummary ? 'Cerrar' : 'Cancelar' }}
        </button>
        <button
          v-if="selectedFile && !resultSummary"
          @click="uploadFile"
          :disabled="uploading"
          class="px-5 py-2.5 bg-blue-900 hover:bg-blue-950 text-white text-xs font-bold rounded-xl transition shadow-md flex items-center space-x-2 cursor-pointer disabled:opacity-50"
        >
          <svg v-if="uploading" class="animate-spin w-4 h-4 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <span>{{ uploading ? 'Procesando Respaldo e Ingesta...' : 'Iniciar Importación Masiva' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  tableName: {
    type: String,
    default: 'planteles'
  },
  initialFile: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'upload-success'])

const fileInputRef = ref(null)
const selectedFile = ref(null)
const isDragging = ref(false)
const uploading = ref(false)
const resultSummary = ref(null)
const errorMessage = ref('')

watch(() => props.initialFile, (newFile) => {
  if (newFile) {
    validateAndSetFile(newFile)
  }
}, { immediate: true })

function triggerFileInput() {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
}

function handleFileSelect(event) {
  const files = event.target.files
  if (files && files.length > 0) {
    validateAndSetFile(files[0])
  }
}

function handleDrop(event) {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files && files.length > 0) {
    validateAndSetFile(files[0])
  }
}

function validateAndSetFile(file) {
  errorMessage.value = ''
  resultSummary.value = null
  const ext = file.name.split('.').pop().toLowerCase()
  if (['xlsx', 'xlsm', 'xls', 'csv'].includes(ext)) {
    selectedFile.value = file
  } else {
    errorMessage.value = 'Formato no soportado. Por favor selecciona un archivo .xlsx, .xlsm, .xls o .csv'
  }
}

async function uploadFile() {
  if (!selectedFile.value) return
  uploading.value = true
  errorMessage.value = ''
  resultSummary.value = null

  try {
    const token = localStorage.getItem('admin_token')
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await axios.post(`/api/admin/data/${props.tableName}/upload-excel`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    resultSummary.value = response.data
    emit('upload-success')
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Error al procesar e importar el archivo Excel.'
  } finally {
    uploading.value = false
  }
}

async function downloadOfficialTemplate() {
  try {
    const token = localStorage.getItem('admin_token')
    const response = await axios.get(`/api/admin/data/download-template/${props.tableName}`, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `PLANTILLA_OFICIAL_${props.tableName.toUpperCase()}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (err) {
    errorMessage.value = 'Error al descargar la plantilla oficial.'
  }
}

function close() {
  selectedFile.value = null
  resultSummary.value = null
  errorMessage.value = ''
  emit('close')
}
</script>
