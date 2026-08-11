<template>
  <!-- Toolbar - Conmutación Oscuro/Claro -->
  <div 
    :class="isDark 
      ? 'bg-white/5 backdrop-blur-md border-white/10' 
      : 'bg-white border-slate-200 shadow-sm'" 
    class="p-3.5 rounded-2xl border transition-colors duration-300 flex flex-col md:flex-row md:items-center justify-between gap-3"
  >
    <!-- Buscador Rápido -->
    <div class="relative max-w-sm w-full">
      <svg class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        placeholder="Buscar en celdas de la tabla..."
        :class="isDark 
          ? 'bg-[#0d1c2d] border-white/10 text-white placeholder-slate-400 focus:border-[#4edea3]/40' 
          : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400 focus:border-blue-900'"
        class="w-full pl-9 pr-4 py-2 border rounded-xl text-xs font-medium focus:outline-none focus:ring-1 transition"
      />
    </div>

    <!-- Botones de Acciones -->
    <div class="flex items-center space-x-2 overflow-x-auto scrollbar-none max-w-full py-0.5 shrink-0">
      <!-- Ctrl+Z / Ctrl+Y -->
      <div 
        :class="isDark ? 'bg-white/5 border-white/10' : 'bg-slate-100/80 border-slate-200/80'" 
        class="flex items-center border p-1 rounded-xl space-x-1"
      >
        <button
          @click="$emit('undo')"
          :disabled="!canUndo"
          title="Deshacer último cambio (Ctrl+Z)"
          :class="isDark 
            ? 'hover:bg-white/10 text-slate-300' 
            : 'hover:bg-white text-slate-700'"
          class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition inline-flex items-center space-x-1 cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-transparent"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6-6m-6 6l6 6"/>
          </svg>
          <span class="hidden sm:inline">Deshacer</span>
        </button>

        <button
          @click="$emit('redo')"
          :disabled="!canRedo"
          title="Rehacer cambio (Ctrl+Y)"
          :class="isDark 
            ? 'hover:bg-white/10 text-slate-300' 
            : 'hover:bg-white text-slate-700'"
          class="px-2.5 py-1.5 text-xs font-bold rounded-lg transition inline-flex items-center space-x-1 cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-transparent"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10H11a8 8 0 00-8 8v2m18-10l-6-6m6 6l-6 6"/>
          </svg>
          <span class="hidden sm:inline">Rehacer</span>
        </button>
      </div>

      <!-- Eliminar seleccionadas -->
      <button
        v-if="selectedCount > 0"
        @click="$emit('delete-selected')"
        class="px-3.5 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/30 text-xs font-extrabold rounded-xl transition inline-flex items-center space-x-1.5 cursor-pointer animate-fade-in"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        <span>Eliminar ({{ selectedCount }})</span>
      </button>

      <!-- Importar Excel -->
      <button
        @click="$emit('open-dropzone')"
        :class="isDark 
          ? 'bg-[#7bd0ff]/10 hover:bg-[#7bd0ff]/20 text-[#7bd0ff] border-[#7bd0ff]/30' 
          : 'bg-blue-50 hover:bg-blue-100 text-blue-900 border-blue-200'"
        class="px-3.5 py-2 border text-xs font-bold rounded-xl transition inline-flex items-center space-x-1.5 cursor-pointer"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <span class="hidden sm:inline">Importar</span>
      </button>

      <!-- Exportar Excel -->
      <button
        @click="$emit('export-excel')"
        :class="isDark 
          ? 'bg-[#4edea3]/10 hover:bg-[#4edea3]/20 text-[#4edea3] border-[#4edea3]/30' 
          : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border-emerald-200'"
        class="px-3.5 py-2 border text-xs font-bold rounded-xl transition inline-flex items-center space-x-1.5 cursor-pointer"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
        </svg>
        <span>Exportar .xlsx</span>
      </button>

      <!-- Nueva Fila -->
      <button
        @click="$emit('open-add-modal')"
        :class="isDark ? 'bg-blue-600 hover:bg-blue-500' : 'bg-blue-900 hover:bg-blue-950'"
        class="px-4 py-2 text-white text-xs font-bold rounded-xl transition inline-flex items-center space-x-1.5 shadow-sm cursor-pointer shrink-0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span>Nueva Fila</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '../../composables/useTheme'

const { isDark } = useTheme()

defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  selectedCount: {
    type: Number,
    default: 0
  },
  canUndo: {
    type: Boolean,
    default: false
  },
  canRedo: {
    type: Boolean,
    default: false
  }
})

defineEmits([
  'update:searchQuery',
  'export-excel',
  'open-add-modal',
  'open-dropzone',
  'delete-selected',
  'undo',
  'redo'
])
</script>
