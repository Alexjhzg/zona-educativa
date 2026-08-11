<template>
  <div 
    :class="isDark 
      ? 'bg-slate-900/60 backdrop-blur-xl border-slate-800 shadow-2xl' 
      : 'bg-slate-50/80 border-slate-200/80 shadow-sm'"
    class="w-full border rounded-2xl p-6 transition-all duration-300"
  >
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div 
          :class="isDark 
            ? 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400' 
            : 'bg-cyan-100/70 border-cyan-200 text-cyan-700'"
          class="p-2.5 rounded-xl border shadow-inner"
        >
          <UploadCloud class="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="text-lg font-bold tracking-wide">Importación de Datos Excel</h3>
          <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs">Actualiza o recarga la base de datos de planteles arrastrando tu archivo (.xlsx, .xlsm)</p>
        </div>
      </div>
      <span 
        :class="isDark 
          ? 'bg-cyan-950/60 border-cyan-500/30 text-cyan-300' 
          : 'bg-cyan-100/80 border-cyan-300 text-cyan-900'"
        class="px-2.5 py-1 text-xs font-semibold rounded-full border"
      >
        Modo Upsert
      </span>
    </div>

    <!-- Drag & Drop Zone -->
    <div
      @dragover.prevent="onDragOver"
      @dragenter.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
      :class="[
        'relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 group',
        isDragging
          ? 'border-cyan-400 bg-cyan-500/10 shadow-[0_0_30px_rgba(6,182,212,0.15)] scale-[1.01]'
          : isDark
            ? 'border-slate-700/80 hover:border-cyan-500/50 bg-slate-950/40 hover:bg-slate-900/40'
            : 'border-slate-300 hover:border-cyan-600/50 bg-white hover:bg-cyan-50/20'
      ]"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".xlsx, .xlsm, .xls"
        class="hidden"
        @change="onFileSelected"
      />

      <!-- Content State: Idle / Dragging -->
      <div v-if="!loading && !result" class="flex flex-col items-center justify-center space-y-3">
        <div 
          :class="isDark 
            ? 'bg-gradient-to-tr from-slate-800 to-slate-900 border-slate-700' 
            : 'bg-gradient-to-tr from-slate-100 to-white border-slate-200 shadow-xs'"
          class="w-14 h-14 rounded-2xl flex items-center justify-center border group-hover:scale-110 transition-transform duration-300 shadow-lg"
        >
          <FileSpreadsheet :class="isDark ? 'text-cyan-400 group-hover:text-cyan-300' : 'text-cyan-600 group-hover:text-cyan-700'" class="w-7 h-7" />
        </div>
        <div>
          <p :class="isDark ? 'text-slate-200' : 'text-slate-800'" class="text-sm font-medium">
            <span :class="isDark ? 'text-cyan-400' : 'text-cyan-700'" class="font-semibold underline underline-offset-4">Haz clic para seleccionar</span> o arrastra tu archivo aquí
          </p>
          <p :class="isDark ? 'text-slate-500' : 'text-slate-400'" class="text-xs mt-1">Soporta formatos oficial Excel: .xlsx, .xlsm (Hoja 'planteles')</p>
        </div>
      </div>

      <!-- Content State: Loading -->
      <div v-else-if="loading" class="flex flex-col items-center justify-center space-y-3 py-2">
        <Loader2 class="w-10 h-10 text-cyan-500 animate-spin" />
        <div>
          <p :class="isDark ? 'text-cyan-300' : 'text-cyan-800'" class="text-sm font-semibold animate-pulse">Procesando e Ingestando Datos...</p>
          <p :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs mt-1">Analizando filas y actualizando registros de planteles</p>
        </div>
      </div>

      <!-- Content State: Result Success -->
      <div v-else-if="result && !errorMessage" class="flex flex-col items-center justify-center space-y-3">
        <div class="w-12 h-12 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-500">
          <CheckCircle2 class="w-7 h-7" />
        </div>
        <p class="text-sm font-bold text-emerald-600">¡Importación Procesada Exitosamente!</p>
      </div>

      <!-- Content State: Error -->
      <div v-else-if="errorMessage" class="flex flex-col items-center justify-center space-y-3">
        <div class="w-12 h-12 rounded-full bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-500">
          <AlertCircle class="w-7 h-7" />
        </div>
        <p class="text-sm font-bold text-rose-600">{{ errorMessage }}</p>
      </div>
    </div>

    <!-- Summary Details Card (Shown after import) -->
    <transition enter-active-class="transition duration-300 ease-out" enter-from-class="opacity-0 translate-y-2" enter-to-class="opacity-100 translate-y-0">
      <div 
        v-if="result" 
        :class="isDark 
          ? 'bg-slate-950/80 border-slate-800 text-slate-200' 
          : 'bg-white border-slate-200 text-slate-800 shadow-sm'"
        class="mt-5 p-4 rounded-xl border"
      >
        <div :class="isDark ? 'border-slate-800' : 'border-slate-200'" class="flex items-center justify-between mb-3 border-b pb-2">
          <h4 :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="text-xs font-bold uppercase tracking-wider">Resumen del Proceso ETL</h4>
          <button @click="resetForm" :class="isDark ? 'text-cyan-400 hover:text-cyan-300' : 'text-cyan-700 hover:text-cyan-800'" class="text-xs font-medium transition-colors cursor-pointer">
            Cargar otro archivo
          </button>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-slate-50 border-slate-200'" class="p-3 rounded-lg border text-center">
            <span :class="isDark ? 'text-slate-400' : 'text-slate-500'" class="block text-xs">Filas Evaluadas</span>
            <span :class="isDark ? 'text-white' : 'text-slate-900'" class="text-lg font-extrabold">{{ result.detalles.total_filas }}</span>
          </div>
          <div :class="isDark ? 'bg-emerald-950/40 border-emerald-500/30' : 'bg-emerald-50 border-emerald-200'" class="p-3 rounded-lg border text-center">
            <span class="block text-xs text-emerald-600 font-semibold">Nuevos Creados</span>
            <span class="text-lg font-extrabold text-emerald-700">+{{ result.detalles.creados }}</span>
          </div>
          <div :class="isDark ? 'bg-blue-950/40 border-blue-500/30' : 'bg-blue-50 border-blue-200'" class="p-3 rounded-lg border text-center">
            <span class="block text-xs text-blue-600 font-semibold">Actualizados</span>
            <span class="text-lg font-extrabold text-blue-700">{{ result.detalles.actualizados }}</span>
          </div>
          <div :class="isDark ? 'bg-rose-950/40 border-rose-500/30' : 'bg-rose-50 border-rose-200'" class="p-3 rounded-lg border text-center">
            <span class="block text-xs text-rose-600 font-semibold">Errores</span>
            <span class="text-lg font-extrabold text-rose-700">{{ result.detalles.errores }}</span>
          </div>
        </div>

        <!-- Detail of errors if any -->
        <div v-if="result.detalles.detalles_errores && result.detalles.detalles_errores.length > 0" :class="isDark ? 'bg-rose-950/30 border-rose-900/50' : 'bg-rose-50 border-rose-200'" class="mt-3 p-3 rounded-lg border">
          <p class="text-xs font-bold text-rose-600 mb-1">Detalles de Advertencias/Errores:</p>
          <ul class="text-xs text-rose-700 list-disc list-inside space-y-0.5 max-h-24 overflow-y-auto">
            <li v-for="(err, idx) in result.detalles.detalles_errores" :key="idx">{{ err }}</li>
          </ul>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { useTheme } from '../../composables/useTheme'
import { UploadCloud, FileSpreadsheet, Loader2, CheckCircle2, AlertCircle } from 'lucide-vue-next'

const emit = defineEmits(['imported'])
const adminStore = useAdminStore()
const { isDark } = useTheme()

const fileInput = ref(null)
const isDragging = ref(false)
const loading = ref(false)
const result = ref(null)
const errorMessage = ref('')

const triggerFileInput = () => {
  if (loading.value) return
  fileInput.value.click()
}

const onDragOver = () => {
  isDragging.value = true
}

const onDragLeave = () => {
  isDragging.value = false
}

const validateAndUpload = async (file) => {
  if (!file) return

  const name = file.name.toLowerCase()
  if (!name.endsWith('.xlsx') && !name.endsWith('.xlsm') && !name.endsWith('.xls')) {
    errorMessage.value = 'Formato de archivo no válido. Selecciona un archivo Excel (.xlsx o .xlsm).'
    result.value = null
    return
  }

  errorMessage.value = ''
  result.value = null
  loading.value = true

  try {
    const res = await adminStore.importarExcel(file)
    result.value = res
    emit('imported', res)
  } catch (error) {
    console.error('Error al importar Excel:', error)
    errorMessage.value = error.response?.data?.detail || 'Error en la comunicación con el servidor al procesar el Excel.'
  } finally {
    loading.value = false
  }
}

const onDrop = (e) => {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files && files.length > 0) {
    validateAndUpload(files[0])
  }
}

const onFileSelected = (e) => {
  const files = e.target.files
  if (files && files.length > 0) {
    validateAndUpload(files[0])
  }
}

const resetForm = () => {
  result.value = null
  errorMessage.value = ''
  if (fileInput.value) fileInput.value.value = ''
}
</script>
