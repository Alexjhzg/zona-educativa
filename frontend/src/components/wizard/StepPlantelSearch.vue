<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-blue-900 text-white font-extrabold text-xs flex items-center justify-center shadow-xs">2</span>
          <label class="block text-base font-extrabold text-slate-900">
            Identificación del Plantel <span class="text-red-500">*</span>
          </label>
        </div>
      </div>
      <p class="text-xs text-slate-500 mb-4">Ingresa el Código DEA o Cédula de Identidad completa en uno de los campos para cargar los datos del plantel.</p>

      <!-- Entrada de Búsqueda Lado a Lado -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        <div class="relative">
          <label class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1 flex justify-between">
            <span>Código DEA del Plantel</span>
            <span v-if="Boolean(ciInput || (selectedPlantel && activeSearchSource === 'ci'))" class="text-[10px] text-slate-400 font-semibold lowercase">(Bloqueado)</span>
          </label>
          <input
            :value="deaInput"
            @input="$emit('on-dea-input', $event.target.value)"
            type="text"
            placeholder="Ej. S4152D1608"
            :disabled="Boolean(ciInput || (selectedPlantel && activeSearchSource === 'ci'))"
            :class="[
              Boolean(ciInput || (selectedPlantel && activeSearchSource === 'ci'))
                ? 'bg-slate-100/80 border-slate-200 text-slate-400 cursor-not-allowed select-none opacity-60'
                : 'bg-slate-50 border-slate-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-900/30 focus:border-blue-900 text-slate-900'
            ]"
            class="w-full px-4 py-3 rounded-xl font-mono font-bold text-sm uppercase transition"
          />
        </div>

        <div class="relative">
          <label class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1 flex justify-between">
            <span>Cédula de Identidad</span>
            <span v-if="Boolean(deaInput || (selectedPlantel && activeSearchSource === 'dea'))" class="text-[10px] text-slate-400 font-semibold lowercase">(Bloqueado)</span>
          </label>
          <input
            :value="ciInput"
            @input="$emit('on-ci-input', $event.target.value)"
            type="text"
            placeholder="Ej. 3327755"
            :disabled="Boolean(deaInput || (selectedPlantel && activeSearchSource === 'dea'))"
            :class="[
              Boolean(deaInput || (selectedPlantel && activeSearchSource === 'dea'))
                ? 'bg-slate-100/80 border-slate-200 text-slate-400 cursor-not-allowed select-none opacity-60'
                : 'bg-slate-50 border-slate-200 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-900/30 focus:border-blue-900 text-slate-900'
            ]"
            class="w-full px-4 py-3 rounded-xl font-mono font-bold text-sm uppercase transition"
          />
        </div>
      </div>


      <!-- Card de Plantel Verificado -->
      <div v-if="selectedPlantel" class="mt-4 bg-gradient-to-br from-blue-50/90 via-slate-50 to-indigo-50/80 border border-blue-200/80 rounded-2xl p-5 shadow-xs relative overflow-hidden animate-fade-in space-y-4">
        <div class="flex justify-between items-start">
          <div class="w-full">
            <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 bg-emerald-100 text-emerald-800 font-bold text-[10px] uppercase tracking-wider rounded-md mb-1.5 border border-emerald-200">
              <svg class="w-3 h-3 text-emerald-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
              </svg>
              Plantel Verificado
            </span>
            <h3 class="text-lg font-extrabold font-heading text-slate-900">
              {{ selectedPlantel.plantel }}
            </h3>
            <div class="mt-2 grid grid-cols-2 gap-2 text-xs text-slate-600">
              <div><span class="text-slate-500">Código DEA:</span> <strong class="font-mono text-slate-900">{{ selectedPlantel.codigo_dea }}</strong></div>
              <div><span class="text-slate-500">Director Registrado:</span> <strong class="text-slate-900">{{ selectedPlantel.nombres_contacto || 'N/A' }}</strong></div>
              <div><span class="text-slate-500">Cédula Director:</span> <strong class="font-mono text-slate-900">{{ formatCiDisplay(selectedPlantel.ci_contacto) }}</strong></div>
              <div><span class="text-slate-500">Municipio:</span> <strong class="text-slate-900">{{ selectedPlantel.municipio_nombre }}</strong></div>
            </div>
          </div>
          <button @click="$emit('clear-plantel')" type="button" title="Borrar selección" class="bg-slate-200/80 hover:bg-red-100 hover:text-red-700 text-slate-700 font-bold p-1.5 rounded-lg text-xs transition shrink-0 ml-2 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Botón de Despliegue de Actualización de Director -->
        <div v-if="solicitanteRol === 'DIRECTOR'" class="pt-3 border-t border-slate-200/80">
          <div v-if="!showDirectorUpdateForm" class="flex justify-end items-center">
            <button 
              @click="$emit('open-director-update')" 
              type="button" 
              class="inline-flex items-center space-x-1.5 text-xs font-bold text-blue-900 bg-blue-100/80 hover:bg-blue-200 text-blue-950 px-3 py-1.5 rounded-xl transition border border-blue-200/80 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-blue-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
              </svg>
              <span>Actualizar Datos del Director</span>
            </button>
          </div>

          <!-- Sub-Formulario Desplegable -->
          <SubFormDirectorUpdate
            v-else
            :model-value="nuevoDirector"
            @update:model-value="$emit('update:nuevo-director', $event)"
            @cancel="$emit('cancel-director-update')"
          />
        </div>
      </div>

      <!-- Mensaje si no fue encontrado -->
      <div v-else-if="searchNotFound" class="mt-3 p-4 bg-amber-50 border border-amber-200/80 rounded-2xl text-center text-xs text-amber-800 font-medium animate-fade-in">
        No se encontró ningún plantel registrado con el Código DEA o Cédula ingresada. Por favor verifica la información e intenta de nuevo.
      </div>

      <!-- Mensaje por Defecto -->
      <div v-else class="mt-3 p-4 bg-slate-50 border border-dashed border-slate-200 rounded-2xl text-center text-xs text-slate-400 font-medium">
        Ingresa el Código DEA o Cédula de Identidad completa en uno de los campos para traer los datos del plantel.
      </div>
    </div>

    <!-- Botones de Navegación Paso 2 -->
    <div class="flex justify-between items-center pt-4 border-t border-slate-100">
      <button
        type="button"
        @click="$emit('prev-step')"
        class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-xl transition cursor-pointer"
      >
        ← Anterior
      </button>
      <button
        type="button"
        @click="$emit('next-step')"
        :disabled="!selectedPlantel"
        class="px-6 py-3 bg-blue-900 hover:bg-blue-950 disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold text-sm rounded-xl transition shadow-md shadow-blue-900/10 inline-flex items-center space-x-2 cursor-pointer"
      >
        <span>Siguiente: Datos de Contacto</span>
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import SubFormDirectorUpdate from './SubFormDirectorUpdate.vue'

defineProps({
  deaInput: String,
  ciInput: String,
  activeSearchSource: String,
  selectedPlantel: Object,
  searchResults: Array,
  loadingSearch: Boolean,
  searchNotFound: Boolean,
  solicitanteRol: String,
  showDirectorUpdateForm: Boolean,
  nuevoDirector: Object
})

defineEmits([
  'on-dea-input',
  'on-ci-input',
  'select-plantel',
  'clear-plantel',
  'open-director-update',
  'cancel-director-update',
  'update:nuevo-director',
  'prev-step',
  'next-step'
])

function formatCiDisplay(ciVal) {
  if (!ciVal) return ''
  return String(ciVal).replace('.0', '').trim()
}
</script>
