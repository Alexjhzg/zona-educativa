<template>
  <div
    v-if="visible"
    :style="{ top: `${y}px`, left: `${x}px` }"
    class="fixed z-50 bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl shadow-xl p-1.5 min-w-[210px] text-xs font-medium text-slate-800 space-y-1 animate-fade-in"
    @click.stop
  >
    <div class="px-3 py-1.5 text-[10px] font-extrabold text-slate-400 uppercase tracking-wider border-b border-slate-100 flex justify-between items-center">
      <span>Opciones</span>
      <span class="bg-blue-50 text-blue-900 px-1.5 py-0.5 rounded font-bold">
        {{ selectedCount }} {{ selectedCount === 1 ? 'fila' : 'filas' }}
      </span>
    </div>

    <button
      @click="$emit('action', 'ver-qr')"
      class="w-full text-left px-3 py-2 hover:bg-emerald-50 text-emerald-700 rounded-xl transition font-bold flex items-center space-x-2 cursor-pointer"
    >
      <QrCode class="w-4 h-4 text-emerald-600 shrink-0" />
      <span>Ver Código QR</span>
    </button>

    <button
      @click="$emit('action', 'copiar')"
      class="w-full text-left px-3 py-2 hover:bg-slate-100 rounded-xl transition flex items-center space-x-2 cursor-pointer"
    >
      <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
      </svg>
      <span>Copiar Valor de Celda</span>
    </button>

    <button
      @click="$emit('action', 'eliminar')"
      class="w-full text-left px-3 py-2 hover:bg-red-50 text-red-600 rounded-xl transition font-bold flex items-center space-x-2 cursor-pointer"
    >
      <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
      </svg>
      <span>Eliminar {{ selectedCount > 1 ? selectedCount + ' Filas' : 'Fila' }}</span>
    </button>
  </div>
</template>

<script setup>
import { QrCode } from 'lucide-vue-next'

defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  selectedCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['action'])
</script>
