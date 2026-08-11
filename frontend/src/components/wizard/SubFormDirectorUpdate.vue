<template>
  <div class="p-4 bg-amber-50/90 border border-amber-200 rounded-xl space-y-3 animate-fade-in text-xs">
    <div class="flex justify-between items-center">
      <span class="font-bold text-amber-900 flex items-center space-x-1.5">
        <svg class="w-4 h-4 text-amber-700 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <span>Ingresa los datos actualizados del Director a corroborar:</span>
      </span>
      <button 
        @click="$emit('cancel')" 
        type="button" 
        class="text-xs font-bold text-amber-800 hover:text-amber-950 underline cursor-pointer"
      >
        Conservar datos actuales ✕
      </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div>
        <label class="block text-[11px] font-bold text-amber-900 mb-1">Nombre Completo Director</label>
        <input
          :value="modelValue.nombre"
          @input="updateField('nombre', $event.target.value, cleanNombre)"
          type="text"
          placeholder="Nombre y Apellido"
          class="w-full px-3 py-2 bg-white border border-amber-300/80 rounded-lg text-slate-900 font-medium text-xs focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 focus:outline-none shadow-xs"
        />
      </div>
      <div>
        <label class="block text-[11px] font-bold text-amber-900 mb-1">Cédula del Director</label>
        <input
          :value="modelValue.ci"
          @input="updateField('ci', $event.target.value, cleanCi)"
          type="text"
          placeholder="Ej. V-12345678"
          class="w-full px-3 py-2 bg-white border border-amber-300/80 rounded-lg text-slate-900 font-medium text-xs focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 focus:outline-none shadow-xs"
        />
      </div>
      <div>
        <label class="block text-[11px] font-bold text-amber-900 mb-1">Teléfono Director</label>
        <input
          :value="modelValue.telefono"
          @input="updateField('telefono', $event.target.value, cleanTelefono)"
          type="tel"
          placeholder="Ej. 0414-1234567"
          class="w-full px-3 py-2 bg-white border border-amber-300/80 rounded-lg text-slate-900 font-medium text-xs focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 focus:outline-none shadow-xs"
        />
      </div>
      <div>
        <label class="block text-[11px] font-bold text-amber-900 mb-1">Correo Director</label>
        <input
          :value="modelValue.email"
          @input="updateField('email', $event.target.value, val => val)"
          type="email"
          placeholder="director@educacion.gob.ve"
          class="w-full px-3 py-2 bg-white border border-amber-300/80 rounded-lg text-slate-900 font-medium text-xs focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 focus:outline-none shadow-xs"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'cancel'])

function cleanNombre(val) {
  return String(val || '').replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '')
}

function cleanCi(val) {
  return String(val || '').replace(/[^0-9veVE-]/g, '').toUpperCase()
}

function cleanTelefono(val) {
  return String(val || '').replace(/[^0-9-\s]/g, '')
}

function updateField(key, rawValue, cleanerFn) {
  const cleaned = cleanerFn(rawValue)
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: cleaned
  })
}
</script>
