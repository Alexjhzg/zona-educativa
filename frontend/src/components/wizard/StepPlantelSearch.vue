<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-blue-900 text-white font-extrabold text-xs flex items-center justify-center shadow-xs">2</span>
          <label class="block text-base font-extrabold text-slate-900">
            Identificación y Búsqueda del Plantel <span class="text-red-500">*</span>
          </label>
        </div>
      </div>
      <p class="text-xs text-slate-500 mb-4">Ingresa el Código DEA o la Cédula de Identidad en uno de los campos para autocompletar con navegación de teclado.</p>

      <!-- Búsqueda Lado a Lado con Autocompletado Headless UI -->
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

      <!-- Indicador de Carga -->
      <div v-if="loadingSearch" class="mt-2 text-xs text-blue-900 font-bold animate-pulse flex items-center space-x-1">
        <svg class="animate-spin w-4 h-4 text-blue-900 mr-1" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        <span>Buscando datos del plantel...</span>
      </div>

      <!-- Combobox Dropdown Headless UI con Selección por Teclado -->
      <Combobox v-if="searchResults.length > 0 && !selectedPlantel" @update:modelValue="$emit('select-plantel', $event)" as="div" class="mt-2 relative z-50">
        <ComboboxOptions static class="max-h-60 overflow-y-auto bg-white border border-slate-200 rounded-2xl shadow-2xl divide-y divide-slate-100 focus:outline-none">
          <ComboboxOption
            v-for="item in searchResults"
            :key="item.id"
            :value="item"
            v-slot="{ active, selected }"
            as="template"
          >
            <li
              :class="[
                'p-3.5 cursor-pointer transition flex justify-between items-center text-sm',
                active ? 'bg-blue-900 text-white' : 'hover:bg-blue-50 text-slate-900'
              ]"
            >
              <div>
                <div class="flex items-center space-x-2">
                  <span
                    :class="active ? 'bg-white/20 text-white border-white/30' : 'bg-blue-50 text-blue-900 border-blue-100'"
                    class="font-mono font-extrabold px-2 py-0.5 rounded text-xs border"
                  >
                    DEA: {{ item.codigo_dea }}
                  </span>
                  <span
                    v-if="item.ci_contacto"
                    :class="active ? 'bg-white/10 text-white' : 'bg-slate-100 text-slate-600'"
                    class="font-mono font-bold px-2 py-0.5 rounded text-xs"
                  >
                    C.I: {{ formatCiDisplay(item.ci_contacto) }}
                  </span>
                </div>
                <div class="font-bold mt-1" :class="active ? 'text-white' : 'text-slate-900'">{{ item.plantel }}</div>
                <div class="text-xs mt-0.5" :class="active ? 'text-blue-100' : 'text-slate-500'">
                  Director: <strong>{{ item.nombres_contacto || 'No registrado' }}</strong> | {{ item.municipio_nombre }}
                </div>
              </div>
              <span
                :class="[
                  getEstatusBadgeClass(item.estatus_qr),
                  active ? 'ring-1 ring-white/50' : ''
                ]"
                class="px-2.5 py-1 text-xs font-bold rounded-lg shrink-0 ml-2"
              >
                {{ item.estatus_qr }}
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </Combobox>

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
          <button @click="$emit('clear-plantel')" type="button" class="bg-slate-200/80 hover:bg-red-100 hover:text-red-700 text-slate-700 font-bold p-1.5 rounded-lg text-xs transition shrink-0 ml-2 cursor-pointer">
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

      <div v-else class="mt-3 p-4 bg-slate-50 border border-dashed border-slate-200 rounded-2xl text-center text-xs text-slate-400 font-medium">
        Ingresa el Código DEA o la Cédula en cualquiera de los dos campos superiores para buscar y seleccionar el plantel.
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
import { Combobox, ComboboxOptions, ComboboxOption } from '@headlessui/vue'
import SubFormDirectorUpdate from './SubFormDirectorUpdate.vue'

defineProps({
  deaInput: String,
  ciInput: String,
  activeSearchSource: String,
  selectedPlantel: Object,
  searchResults: Array,
  loadingSearch: Boolean,
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

function getEstatusBadgeClass(estatus) {
  if (estatus === 'QR SEGEN') return 'bg-emerald-100 text-emerald-800'
  if (estatus === 'REPONER QR') return 'bg-amber-100 text-amber-800'
  return 'bg-slate-100 text-slate-700'
}
</script>
