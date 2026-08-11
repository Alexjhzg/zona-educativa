<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <div class="flex items-center space-x-2.5 mb-3">
        <span class="w-7 h-7 rounded-xl bg-blue-900 text-white font-extrabold text-xs flex items-center justify-center shadow-xs">1</span>
        <label class="block text-base font-extrabold text-slate-900">
          ¿Quién realiza la solicitud? <span class="text-red-500">*</span>
        </label>
      </div>
      <p class="text-xs text-slate-500 mb-5">Selecciona tu perfil institucional para personalizar la búsqueda del plantel y formulario de contacto.</p>

      <!-- Tarjetas de Selección de Rol con Iconos SVG -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div 
          v-for="rol in rolesOptions" 
          :key="rol.value"
          @click="selectRol(rol.value)"
          :class="[
            modelValue === rol.value 
              ? 'bg-gradient-to-br from-blue-900 to-indigo-950 text-white border-blue-900 shadow-xl scale-[1.02]' 
              : 'bg-white text-slate-800 border-slate-200/90 hover:border-blue-900/40 hover:bg-slate-50/80 shadow-xs'
          ]"
          class="flex items-center justify-between p-4.5 border-2 rounded-2xl cursor-pointer text-xs md:text-sm font-bold transition-all duration-200"
        >
          <div class="flex items-center space-x-3.5">
            <div
              :class="modelValue === rol.value ? 'bg-white/20 text-white' : 'bg-blue-50 text-blue-900'"
              class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 transition"
            >
              <svg v-if="rol.value === 'DIRECTOR'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
            </div>
            <div>
              <span class="block font-extrabold text-sm leading-tight">{{ rol.label }}</span>
              <span class="block text-[11px] font-normal mt-0.5" :class="modelValue === rol.value ? 'text-blue-100' : 'text-slate-500'">{{ rol.desc }}</span>
            </div>
          </div>

          <span class="w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ml-2" :class="modelValue === rol.value ? 'border-white bg-white/20' : 'border-slate-300'">
            <span v-if="modelValue === rol.value" class="w-2.5 h-2.5 rounded-full bg-white"></span>
          </span>
        </div>
      </div>
    </div>

    <!-- Botón de Siguiente Paso 1 -->
    <div class="flex justify-end pt-4 border-t border-slate-100">
      <button
        type="button"
        @click="$emit('next-step')"
        :disabled="!modelValue"
        class="px-6 py-3 bg-blue-900 hover:bg-blue-950 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white font-bold text-sm rounded-xl transition shadow-md shadow-blue-900/10 inline-flex items-center space-x-2 cursor-pointer"
      >
        <span>Siguiente: Buscar Plantel</span>
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'next-step'])

const rolesOptions = [
  { value: 'DIRECTOR', label: 'Director(a) de Plantel', desc: 'Representante oficial con firma autorizada' },
  { value: 'REPRESENTANTE', label: 'Representante de Institución', desc: 'Personal administrativo o técnico delegado' }
]

function selectRol(val) {
  emit('update:modelValue', val)
}
</script>
