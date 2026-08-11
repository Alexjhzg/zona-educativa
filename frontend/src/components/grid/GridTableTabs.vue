<template>
  <!-- Tabs de Tablas - Responsivo para Móviles y Escritorio -->
  <div 
    :class="isDark 
      ? 'bg-white/5 backdrop-blur-md border-white/10' 
      : 'bg-white border-slate-200 shadow-sm'" 
    class="inline-flex items-center p-1.5 rounded-2xl border transition-colors duration-300 gap-1.5 overflow-x-auto scrollbar-none w-fit max-w-full"
  >
    <div class="flex items-center space-x-1.5 shrink-0 overflow-x-auto scrollbar-none py-0.5">
      <!-- Tab Planteles -->
      <button
        @click="$emit('switch-table', 'planteles')"
        :class="[
          activeTable === 'planteles'
            ? (isDark ? 'bg-[#4edea3] text-[#051424] shadow-md font-extrabold' : 'bg-blue-900 text-white shadow-md shadow-blue-900/20 font-extrabold')
            : (isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white font-medium' : 'text-slate-600 hover:bg-slate-100 font-medium')
        ]"
        class="px-3.5 sm:px-4 py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center space-x-2 shrink-0 whitespace-nowrap"
      >
        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
        </svg>
        <span>Planteles {{ activeTable === 'planteles' ? `(${totalRows})` : '(988)' }}</span>
      </button>

      <!-- Tab Solicitudes QR -->
      <button
        @click="$emit('switch-table', 'solicitudes_qr')"
        :class="[
          activeTable === 'solicitudes_qr'
            ? (isDark ? 'bg-[#4edea3] text-[#051424] shadow-md font-extrabold' : 'bg-blue-900 text-white shadow-md shadow-blue-900/20 font-extrabold')
            : (isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white font-medium' : 'text-slate-600 hover:bg-slate-100 font-medium')
        ]"
        class="px-3.5 sm:px-4 py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center space-x-2 shrink-0 whitespace-nowrap"
      >
        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span>Solicitudes QR {{ activeTable === 'solicitudes_qr' ? `(${totalRows})` : '' }}</span>
      </button>

      <!-- Tab Municipios -->
      <button
        @click="$emit('switch-table', 'municipios')"
        :class="[
          activeTable === 'municipios'
            ? (isDark ? 'bg-[#4edea3] text-[#051424] shadow-md font-extrabold' : 'bg-blue-900 text-white shadow-md shadow-blue-900/20 font-extrabold')
            : (isDark ? 'text-slate-300 hover:bg-white/10 hover:text-white font-medium' : 'text-slate-600 hover:bg-slate-100 font-medium')
        ]"
        class="px-3.5 sm:px-4 py-2 rounded-xl text-xs transition-all cursor-pointer flex items-center space-x-2 shrink-0 whitespace-nowrap"
      >
        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
        </svg>
        <span>Municipios {{ activeTable === 'municipios' ? `(${totalRows})` : '' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '../../composables/useTheme'

const { isDark } = useTheme()

defineProps({
  activeTable: {
    type: String,
    required: true
  },
  totalRows: {
    type: Number,
    default: 0
  }
})

defineEmits(['switch-table'])
</script>
<style scoped>
/* Ocultar barra de scroll en contenedores táctiles */
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
