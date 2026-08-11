<template>
  <div 
    v-if="isOpen" 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md overflow-y-auto"
    @click.self="closeModal"
  >
    <div 
      :class="isDark 
        ? 'bg-[#0b1726] border-white/10 text-white shadow-2xl' 
        : 'bg-white border-slate-200 text-slate-900 shadow-2xl'" 
      class="relative w-full max-w-2xl rounded-3xl border p-6 md:p-8 transition-all overflow-hidden my-8 flex flex-col"
    >
      <!-- Header bar: [spacer] [← nav centrada →] [X] -->
      <div class="flex items-center justify-between gap-2 mb-5">
        <!-- Spacer izquierdo del mismo ancho que el botón X para centrar la nav -->
        <div class="w-9 shrink-0"></div>

        <!-- Navegación centrada -->
        <div class="flex items-center gap-2">
          <button
            @click="navigatePrev"
            :disabled="currentIndex <= 0"
            :class="[
              isDark ? 'bg-white/5 hover:bg-white/10 border-white/10 text-slate-300 disabled:text-slate-600 disabled:border-white/5' 
                     : 'bg-slate-100 hover:bg-slate-200 border-slate-200 text-slate-600 disabled:text-slate-300 disabled:border-slate-100',
              'flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all cursor-pointer disabled:cursor-not-allowed'
            ]"
          >
            <ChevronLeft class="w-4 h-4 shrink-0" />
            <span class="hidden sm:inline">Anterior</span>
          </button>

          <span class="text-xs font-bold tabular-nums px-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            {{ currentIndex + 1 }}<span class="font-normal opacity-60">/</span>{{ plantelList.length }}
          </span>

          <button
            @click="navigateNext"
            :disabled="currentIndex >= plantelList.length - 1"
            :class="[
              isDark ? 'bg-white/5 hover:bg-white/10 border-white/10 text-slate-300 disabled:text-slate-600 disabled:border-white/5' 
                     : 'bg-slate-100 hover:bg-slate-200 border-slate-200 text-slate-600 disabled:text-slate-300 disabled:border-slate-100',
              'flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all cursor-pointer disabled:cursor-not-allowed'
            ]"
          >
            <span class="hidden sm:inline">Siguiente</span>
            <ChevronRight class="w-4 h-4 shrink-0" />
          </button>
        </div>

        <!-- Botón Cerrar -->
        <button 
          @click="closeModal"
          :class="isDark ? 'text-slate-400 hover:bg-white/10 hover:text-white' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'"
          class="p-2 rounded-full transition-all cursor-pointer shrink-0"
          title="Cerrar"
        >
          <X class="w-5 h-5" />
        </button>
      </div>


      <!-- Modal Header -->
      <div class="mb-6">
        <div class="flex items-center gap-2 mb-1">
          <span 
            :class="isDark ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' : 'bg-purple-100 text-purple-700 border-purple-200'"
            class="px-2.5 py-0.5 text-[10px] font-black rounded-full border uppercase tracking-wider"
          >
            {{ currentPlantel?.codigo_dea || 'S/DEA' }}
          </span>
          <span class="text-xs font-bold text-slate-400">· {{ currentPlantel?.dependencia || 'N/A' }}</span>
        </div>
        <h3 class="text-xl font-black leading-snug line-clamp-2">
          {{ currentPlantel?.plantel || 'Plantel Educativo' }}
        </h3>
        <p class="text-xs text-slate-400 mt-1 font-medium flex items-center gap-1">
          <MapPin class="w-3.5 h-3.5 shrink-0 text-amber-500" />
          <span>{{ currentPlantel?.municipio_nombre || 'Monagas' }}</span>
        </p>
      </div>

      <!-- Grilla de Todos los Códigos QR Asignados -->
      <div class="mb-6">
        <div class="flex justify-between items-center mb-3">
          <label class="text-xs font-extrabold uppercase tracking-wider text-slate-400">
            Códigos QR Asignados:
          </label>
          <span class="text-xs font-bold px-2 py-0.5 rounded-full" :class="isDark ? 'bg-white/10 text-emerald-400' : 'bg-emerald-100 text-emerald-800'">
            {{ activeQrCodesList.length }} {{ activeQrCodesList.length === 1 ? 'Código' : 'Códigos' }}
          </span>
        </div>

        <div v-if="activeQrCodesList.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-[380px] overflow-y-auto pr-1">
          <div
            v-for="qrItem in activeQrCodesList"
            :key="qrItem.key"
            :class="isDark ? 'bg-[#051424] border-white/10 hover:border-emerald-500/40' : 'bg-slate-50 border-slate-200 hover:border-blue-500/40'"
            class="flex flex-col items-center p-4 rounded-2xl border transition-all text-center group"
          >
            <div class="w-full flex justify-between items-center mb-3">
              <span 
                :class="qrItem.badgeClass"
                class="px-2.5 py-0.5 text-[10px] font-black rounded-full border uppercase tracking-wider"
              >
                {{ qrItem.label }}
              </span>
              <!-- Botón descargar PNG de este QR individual -->
              <div class="flex items-center gap-1">
                <button
                  @click="compartirQR(qrItem)"
                  class="flex items-center gap-1 px-2 py-0.5 rounded-lg text-[10px] font-bold cursor-pointer transition-all"
                  :class="isDark ? 'bg-white/5 hover:bg-emerald-500/20 text-slate-400 hover:text-emerald-300 border border-white/10' : 'bg-slate-100 hover:bg-emerald-100 text-slate-400 hover:text-emerald-700 border border-slate-200'"
                  title="Compartir Código QR"
                >
                  <Share2 class="w-3 h-3 shrink-0" />
                  <span>Compartir</span>
                </button>
                <button
                  @click="generarReporteQR(qrItem)"
                  :disabled="generandoReporte"
                  class="flex items-center gap-1 px-2 py-0.5 rounded-lg text-[10px] font-bold cursor-pointer transition-all disabled:opacity-40 disabled:cursor-wait"
                  :class="isDark ? 'bg-white/5 hover:bg-blue-500/20 text-slate-400 hover:text-blue-300 border border-white/10' : 'bg-slate-100 hover:bg-blue-100 text-slate-400 hover:text-blue-700 border border-slate-200'"
                  title="Descargar PNG"
                >
                  <Download class="w-3 h-3 shrink-0" />
                  <span>PNG</span>
                </button>
              </div>
            </div>

            <div class="p-3 bg-white rounded-2xl shadow-md border border-slate-200 mb-3 inline-block group-hover:scale-105 transition-transform">
              <QrcodeVue 
                :value="qrItem.value" 
                :size="150" 
                level="H" 
                render-as="canvas" 
              />
            </div>

            <div class="w-full mt-auto">
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
                Valor Codificado:
              </p>
              <div 
                :class="isDark ? 'bg-white/5 text-[#4edea3] border-white/10' : 'bg-white text-blue-900 border-slate-200'"
                class="px-3 py-1.5 rounded-xl border font-mono text-xs font-black break-all shadow-inner select-all"
              >
                {{ qrItem.value }}
              </div>
            </div>
          </div>
        </div>

        <div v-else :class="isDark ? 'bg-[#051424] border-white/10' : 'bg-slate-50 border-slate-200'" class="p-8 rounded-2xl border text-center">
          <AlertCircle class="w-10 h-10 text-amber-400 mx-auto mb-2" />
          <p class="text-sm font-bold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
            No posee códigos QR asignados
          </p>
          <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
            Puedes agregar un código QR personalizado utilizando la opción a continuación.
          </p>
        </div>
      </div>

      <!-- Agregar Código Personalizado -->
      <div class="pt-3 border-t" :class="isDark ? 'border-white/10' : 'border-slate-200'">
        <div v-if="!showNewCodeForm" class="flex justify-between items-center">
          <span class="text-xs text-slate-400 font-medium">¿Deseas registrar otro código histórico?</span>
          <button 
            @click="showNewCodeForm = true" 
            class="text-xs font-bold text-[#4edea3] hover:underline flex items-center gap-1 cursor-pointer"
          >
            <Plus class="w-4 h-4" />
            <span>Agregar Código</span>
          </button>
        </div>

        <div v-else class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-xs font-bold text-slate-300">Registrar Código Personalizado:</label>
            <button @click="showNewCodeForm = false" class="text-xs text-slate-400 hover:text-white cursor-pointer">Cancelar</button>
          </div>
          <div class="flex gap-2">
            <input 
              v-model="customLabel" 
              type="text" 
              placeholder="Ej: QR JULIO 2026" 
              :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white' : 'bg-slate-100 border-slate-200 text-slate-900'"
              class="w-1/3 border rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-[#4edea3]"
            />
            <input 
              v-model="customValue" 
              type="text" 
              placeholder="Ej: SEGEN-2026-9999" 
              :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white' : 'bg-slate-100 border-slate-200 text-slate-900'"
              class="w-2/3 border rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-[#4edea3]"
            />
          </div>
          <button 
            @click="saveCustomQrCode" 
            class="w-full bg-[#4edea3] text-[#051424] font-extrabold py-2 rounded-xl text-xs hover:bg-[#6ffbbe] transition-all cursor-pointer shadow-sm"
          >
            Guardar Código
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import QrcodeVue from 'qrcode.vue'
import QRCode from 'qrcode'
import { X, MapPin, AlertCircle, Plus, ChevronLeft, ChevronRight, Download, Share2 } from 'lucide-vue-next'
import { useTheme } from '../../composables/useTheme'
import { useModalKeyboard } from '../../composables/useModalKeyboard'
import { useQrReport } from '../../composables/useQrReport'
import { toast } from 'vue3-toastify'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  plantel: {
    type: Object,
    default: () => null
  },
  plantelList: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'save-custom-qr'])

const { isDark } = useTheme()
const { generandoReporte, generarReporteQR: generarReporteQRFn } = useQrReport()

const showNewCodeForm = ref(false)
const customLabel = ref('')
const customValue = ref('')
const customQrMap = ref({})

// Índice actual en la lista
const currentIndex = ref(0)

// Plantel actualmente visible
const currentPlantel = ref(null)

// Sincronizar cuando el prop plantel cambia
watch(() => props.plantel, (newPlantel) => {
  if (!newPlantel) return
  currentPlantel.value = newPlantel
  showNewCodeForm.value = false
  customLabel.value = ''
  customValue.value = ''
  customQrMap.value = {}

  const idx = props.plantelList.findIndex(p => p.id === newPlantel.id)
  currentIndex.value = idx >= 0 ? idx : 0
}, { immediate: true })

// Navegar al registro anterior
const navigatePrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
    currentPlantel.value = props.plantelList[currentIndex.value]
    resetForm()
  }
}

// Navegar al registro siguiente
const navigateNext = () => {
  if (currentIndex.value < props.plantelList.length - 1) {
    currentIndex.value += 1
    currentPlantel.value = props.plantelList[currentIndex.value]
    resetForm()
  }
}

const closeModal = () => {
  emit('close')
}

// Teclado abstracto
useModalKeyboard(() => props.isOpen, {
  onLeft: navigatePrev,
  onRight: navigateNext,
  onEscape: closeModal
})

const resetForm = () => {
  showNewCodeForm.value = false
  customLabel.value = ''
  customValue.value = ''
  customQrMap.value = {}
}

const activeQrCodesList = computed(() => {
  const p = currentPlantel.value || {}
  const list = []

  if (p.qr_segen) {
    list.push({
      key: 'segen',
      label: 'QR SEGEN',
      value: p.qr_segen,
      badgeClass: isDark.value ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' : 'bg-emerald-100 text-emerald-800 border-emerald-200'
    })
  }

  if (p.qr_director) {
    list.push({
      key: 'director',
      label: 'QR DIRECTOR',
      value: p.qr_director,
      badgeClass: isDark.value ? 'bg-blue-500/20 text-blue-300 border-blue-500/30' : 'bg-blue-100 text-blue-800 border-blue-200'
    })
  }

  if (p.qr_director_sep) {
    list.push({
      key: 'director_sep',
      label: 'QR DIRECTOR SEP',
      value: p.qr_director_sep,
      badgeClass: isDark.value ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' : 'bg-amber-100 text-amber-800 border-amber-200'
    })
  }

  if (p.qr_director_jul_2026) {
    list.push({
      key: 'director_jul_2026',
      label: 'QR DIRECTOR JUL 2026',
      value: p.qr_director_jul_2026,
      badgeClass: isDark.value ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' : 'bg-purple-100 text-purple-800 border-purple-200'
    })
  }

  Object.keys(customQrMap.value).forEach(k => {
    list.push({
      key: k,
      label: customQrMap.value[k].label,
      value: customQrMap.value[k].value,
      badgeClass: isDark.value ? 'bg-sky-500/20 text-sky-300 border-sky-500/30' : 'bg-sky-100 text-sky-800 border-sky-200'
    })
  })

  return list
})

const generarReporteQR = (qrItem) => {
  generarReporteQRFn(qrItem, currentPlantel)
}

const compartirQR = async (qrItem) => {
  const plantelNombre = currentPlantel.value?.plantel || 'Plantel Educativo'
  const dea = currentPlantel.value?.codigo_dea || ''
  
  try {
    const canvas = document.createElement('canvas')
    canvas.width = 300
    canvas.height = 360
    const ctx = canvas.getContext('2d')

    // Fondo blanco
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, 300, 360)

    // Nombre del plantel
    ctx.fillStyle = '#0f172a'
    ctx.font = 'bold 14px Inter, Arial, sans-serif'
    ctx.textAlign = 'center'
    let nombre = `${plantelNombre} (${dea})`
    while (ctx.measureText(nombre).width > 280 && nombre.length > 10) {
      nombre = nombre.slice(0, -1)
    }
    ctx.fillText(nombre, 150, 25)

    // QR Data
    const qrDataUrl = await QRCode.toDataURL(qrItem.value, {
      width: 250,
      margin: 1,
      errorCorrectionLevel: 'H'
    })

    const img = new Image()
    img.src = qrDataUrl
    await new Promise(res => { img.onload = res })
    ctx.drawImage(img, 25, 40, 250, 250)

    // Etiqueta y Valor
    ctx.fillStyle = '#475569'
    ctx.font = 'bold 12px Inter, Arial, sans-serif'
    ctx.fillText(qrItem.label, 150, 310)

    ctx.fillStyle = '#0284c7'
    ctx.font = 'bold 11px monospace'
    ctx.fillText(qrItem.value, 150, 335)

    // Convertir canvas a Blob y crear File object
    canvas.toBlob(async (blob) => {
      if (!blob) return
      const filename = `QR_${qrItem.key}_${dea || 'plantel'}.png`
      const imageFile = new File([blob], filename, { type: 'image/png' })

      if (navigator.canShare && navigator.canShare({ files: [imageFile] })) {
        try {
          await navigator.share({
            files: [imageFile],
            title: `Código QR ${qrItem.label}`,
            text: `Código QR de ${plantelNombre}`
          })
          toast.success('¡Imagen del Código QR compartida!')
        } catch (err) {
          if (err.name !== 'AbortError') {
            descargarBlob(blob, filename)
          }
        }
      } else {
        descargarBlob(blob, filename)
      }
    }, 'image/png')

  } catch (err) {
    console.error(err)
    toast.error('Error al generar la imagen del QR para compartir')
  }
}

const descargarBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
  toast.info('Imagen descargada para compartir.')
}

const saveCustomQrCode = () => {
  if (!customLabel.value.trim() || !customValue.value.trim()) {
    toast.warning('Ingresa la etiqueta y el código QR')
    return
  }

  const key = 'custom_' + Date.now()
  customQrMap.value[key] = {
    label: customLabel.value.trim().toUpperCase(),
    value: customValue.value.trim()
  }

  toast.success(`Código QR "${customLabel.value.trim()}" agregado visualmente`)
  showNewCodeForm.value = false
  customLabel.value = ''
  customValue.value = ''
}
</script>
