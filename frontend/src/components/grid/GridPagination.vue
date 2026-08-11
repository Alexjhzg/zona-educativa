<template>
  <div class="p-4 bg-slate-50 border-t border-slate-200 flex justify-between items-center text-xs text-slate-500 font-medium">
    <span>
      Mostrando {{ rowsLength }} de {{ totalRows }} filas 
      (Celda seleccionada: Fila {{ focusedRow + 1 }}, Columna {{ focusedCol + 1 }})
    </span>
    <div class="flex space-x-2">
      <button
        @click="$emit('prev-page')"
        :disabled="skip === 0"
        class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg font-bold disabled:opacity-40 hover:bg-slate-100 transition cursor-pointer"
      >
        ← Anterior
      </button>
      <button
        @click="$emit('next-page')"
        :disabled="skip + limit >= totalRows"
        class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg font-bold disabled:opacity-40 hover:bg-slate-100 transition cursor-pointer"
      >
        Siguiente →
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  rowsLength: Number,
  totalRows: Number,
  skip: Number,
  limit: Number,
  focusedRow: Number,
  focusedCol: Number
})

defineEmits(['prev-page', 'next-page'])
</script>
