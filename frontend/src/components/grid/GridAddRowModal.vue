<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-fade-in overflow-y-auto">
    <div 
      :class="isDark 
        ? 'bg-[#0b1726] border-white/10 text-white shadow-2xl' 
        : 'bg-white border-slate-200 text-slate-900 shadow-2xl'"
      class="relative rounded-3xl max-w-2xl w-full p-6 md:p-8 space-y-6 border transition-all my-8 shadow-2xl"
    >
      <!-- Encabezado del Modal -->
      <div class="flex justify-between items-center border-b pb-4" :class="isDark ? 'border-white/10' : 'border-slate-100'">
        <div class="flex items-center space-x-3">
          <div :class="isDark ? 'bg-[#4edea3]/15 text-[#4edea3]' : 'bg-blue-100 text-blue-900'" class="p-2.5 rounded-2xl shrink-0">
            <Plus class="w-5 h-5" />
          </div>
          <div>
            <h3 class="text-lg font-black tracking-tight" :class="isDark ? 'text-white' : 'text-slate-900'">
              Nuevo Registro en {{ activeTableLabel }}
            </h3>
            <p class="text-xs text-slate-400 font-medium mt-0.5">
              Busca una institución para autocompletar o ingresa los datos manualmente.
            </p>
          </div>
        </div>
        <button 
          @click="$emit('close')" 
          :class="isDark ? 'text-slate-400 hover:bg-white/10 hover:text-white' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'"
          class="p-2 rounded-full transition cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Buscador de Auto-completado de Institución -->
      <div 
        :class="isDark ? 'bg-[#051424] border-white/10' : 'bg-slate-50 border-slate-200'"
        class="p-4 rounded-2xl border space-y-3 relative"
      >
        <div class="flex items-center justify-between">
          <label class="text-xs font-extrabold uppercase tracking-wider text-[#4edea3] flex items-center gap-1.5">
            <Search class="w-3.5 h-3.5" />
            <span>Autocompletar mediante Búsqueda de Plantel</span>
          </label>
          <span v-if="selectedPlantel" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            ✓ Plantel Vinculado
          </span>
        </div>

        <div class="relative">
          <input 
            v-model="searchTerm"
            @focus="showDropdown = true"
            type="text"
            placeholder="Escribe el nombre del plantel o Código DEA..."
            :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white placeholder-slate-500 focus:border-[#4edea3]' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400 focus:border-blue-900'"
            class="w-full px-4 py-2.5 border rounded-xl text-xs font-semibold focus:outline-none focus:ring-1 transition-all"
          />

          <!-- Menú desplegable de coincidencias -->
          <div 
            v-if="showDropdown && filteredPlanteles.length > 0"
            :class="isDark ? 'bg-[#0b1726] border-white/10 text-white' : 'bg-white border-slate-200 text-slate-900 shadow-xl'"
            class="absolute left-0 right-0 top-full mt-2 rounded-2xl border max-h-56 overflow-y-auto z-50 divide-y divide-white/5 shadow-2xl"
          >
            <button
              v-for="p in filteredPlanteles"
              :key="p.id"
              type="button"
              @click="selectPlantel(p)"
              :class="isDark ? 'hover:bg-white/10' : 'hover:bg-slate-50'"
              class="w-full text-left p-3 text-xs transition flex flex-col cursor-pointer"
            >
              <div class="flex justify-between items-center mb-0.5">
                <span class="font-extrabold text-[#7bd0ff]">{{ p.codigo_dea }}</span>
                <span class="text-[10px] font-bold text-slate-400 uppercase">{{ p.municipio_nombre || p.municipio || 'Monagas' }}</span>
              </div>
              <span class="font-bold truncate" :class="isDark ? 'text-slate-200' : 'text-slate-800'">{{ p.plantel }}</span>
              <span class="text-[10px] text-slate-400">{{ p.nombres_contacto ? 'Director: ' + p.nombres_contacto : 'Sin Director asignado' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Formulario Grilla (2 Columnas) -->
      <form @submit.prevent="$emit('save-new-row')" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[50vh] overflow-y-auto pr-1">
          <div v-for="col in columns.filter(c => c.key !== 'id')" :key="col.key" class="space-y-1">
            <label class="block text-[11px] font-extrabold uppercase tracking-wider text-slate-400">
              {{ col.label }}
            </label>
            
            <select
              v-if="col.type === 'select'"
              :value="newRowForm[col.key]"
              @change="updateField(col.key, $event.target.value)"
              :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white focus:border-[#4edea3]' : 'bg-slate-50 border-slate-300 text-slate-900 focus:border-blue-900'"
              class="w-full px-3.5 py-2.5 border rounded-xl text-xs font-semibold focus:outline-none focus:ring-1 transition-all"
              required
            >
              <option value="" disabled>Seleccione una opción</option>
              <option v-for="opt in col.options" :key="opt" :value="opt" :class="isDark ? 'bg-[#0d1c2d] text-white' : 'bg-white text-slate-900'">{{ opt }}</option>
            </select>

            <input
              v-else
              :value="newRowForm[col.key]"
              @input="updateField(col.key, $event.target.value)"
              type="text"
              :placeholder="'Ingrese ' + col.label.toLowerCase()"
              :class="isDark ? 'bg-[#0d1c2d] border-white/10 text-white placeholder-slate-500 focus:border-[#4edea3]' : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:border-blue-900'"
              class="w-full px-3.5 py-2.5 border rounded-xl text-xs font-semibold focus:outline-none focus:ring-1 transition-all"
              required
            />
          </div>
        </div>

        <!-- Botones de Acción -->
        <div class="flex items-center justify-end space-x-3 pt-4 border-t" :class="isDark ? 'border-white/10' : 'border-slate-100'">
          <button
            type="button"
            @click="$emit('close')"
            :class="isDark ? 'bg-white/10 hover:bg-white/20 text-slate-300' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'"
            class="px-4 py-2.5 text-xs font-bold rounded-xl transition cursor-pointer"
          >
            Cancelar
          </button>

          <button
            type="submit"
            :disabled="savingNewRow"
            :class="isDark ? 'bg-[#4edea3] text-[#003824] hover:bg-[#6ffbbe] shadow-[0_10px_20px_rgba(78,222,163,0.25)]' : 'bg-blue-900 hover:bg-blue-950 text-white shadow-md shadow-blue-900/20'"
            class="px-6 py-2.5 text-xs font-black rounded-xl transition cursor-pointer flex items-center space-x-2 disabled:opacity-50"
          >
            <Loader2 v-if="savingNewRow" class="w-4 h-4 animate-spin" />
            <span>{{ savingNewRow ? 'Guardando Registro...' : 'Crear Registro' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, X, Search, Loader2 } from 'lucide-vue-next'
import { useTheme } from '../../composables/useTheme'

const props = defineProps({
  activeTable: String,
  columns: Array,
  plantelesList: {
    type: Array,
    default: () => []
  },
  newRowForm: Object,
  savingNewRow: Boolean
})

const emit = defineEmits(['close', 'save-new-row', 'update:newRowForm'])

const { isDark } = useTheme()

const searchTerm = ref('')
const showDropdown = ref(false)
const selectedPlantel = ref(null)

const activeTableLabel = computed(() => {
  if (props.activeTable === 'planteles') return 'Planteles Educativos'
  if (props.activeTable === 'solicitudes_qr') return 'Solicitudes de QR'
  if (props.activeTable === 'municipios') return 'Municipios'
  return props.activeTable || 'Tabla'
})

const filteredPlanteles = computed(() => {
  if (!searchTerm.value.trim()) return []
  const q = searchTerm.value.toLowerCase().trim()
  return (props.plantelesList || []).filter(p => 
    (p.plantel && p.plantel.toLowerCase().includes(q)) ||
    (p.codigo_dea && p.codigo_dea.toLowerCase().includes(q)) ||
    (p.municipio_nombre && p.municipio_nombre.toLowerCase().includes(q))
  ).slice(0, 8)
})

function selectPlantel(p) {
  selectedPlantel.value = p
  searchTerm.value = `${p.codigo_dea} - ${p.plantel}`
  showDropdown.value = false

  const updatedForm = { ...props.newRowForm }

  // Mapeo automático inteligente de campos si existen en la tabla activa
  if ('codigo_dea' in updatedForm || props.columns.some(c => c.key === 'codigo_dea')) {
    updatedForm.codigo_dea = p.codigo_dea || ''
  }
  if ('plantel' in updatedForm || props.columns.some(c => c.key === 'plantel')) {
    updatedForm.plantel = p.plantel || ''
  }
  if ('municipio_nombre' in updatedForm || props.columns.some(c => c.key === 'municipio_nombre')) {
    updatedForm.municipio_nombre = p.municipio_nombre || p.municipio || 'MATURIN'
  }
  if ('parroquia_nombre' in updatedForm || props.columns.some(c => c.key === 'parroquia_nombre')) {
    updatedForm.parroquia_nombre = p.parroquia_nombre || p.parroquia || ''
  }
  if ('dependencia' in updatedForm || props.columns.some(c => c.key === 'dependencia')) {
    updatedForm.dependencia = p.dependencia || 'NACIONAL'
  }
  if ('nombres_contacto' in updatedForm || props.columns.some(c => c.key === 'nombres_contacto')) {
    updatedForm.nombres_contacto = p.nombres_contacto || ''
  }
  if ('ci_contacto' in updatedForm || props.columns.some(c => c.key === 'ci_contacto')) {
    updatedForm.ci_contacto = p.ci_contacto || ''
  }
  if ('telefono_contacto' in updatedForm || props.columns.some(c => c.key === 'telefono_contacto')) {
    updatedForm.telefono_contacto = p.telefono_contacto || ''
  }
  if ('email_contacto' in updatedForm || props.columns.some(c => c.key === 'email_contacto')) {
    updatedForm.email_contacto = p.email_contacto || ''
  }
  if ('estatus_qr' in updatedForm || props.columns.some(c => c.key === 'estatus_qr')) {
    updatedForm.estatus_qr = p.estatus_qr || 'SIN QR ASIGNADO'
  }
  if ('plantel_id' in updatedForm || props.columns.some(c => c.key === 'plantel_id')) {
    updatedForm.plantel_id = p.id
  }

  emit('update:newRowForm', updatedForm)
}

function updateField(key, value) {
  emit('update:newRowForm', {
    ...props.newRowForm,
    [key]: value
  })
}
</script>
