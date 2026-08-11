<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <div class="flex items-center space-x-2 mb-3">
        <span class="w-6 h-6 rounded-full bg-blue-900 text-white font-extrabold text-xs flex items-center justify-center shadow-xs">4</span>
        <label class="block text-base font-extrabold text-slate-900">
          Detalles y Confirmación de la Solicitud <span class="text-red-500">*</span>
        </label>
      </div>

      <div class="space-y-4 bg-slate-50/70 p-4 border border-slate-200/80 rounded-2xl">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Tipo de Solicitud</label>
          <select
            :value="form.tipo_solicitud"
            @change="updateFormField('tipo_solicitud', $event.target.value)"
            class="w-full px-4 py-3 bg-white border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-900/30 text-slate-800 font-medium text-sm transition"
            required
          >
            <option value="REPOSICION">Reposición por Pérdida o Deterioro de QR</option>
            <option value="NUEVA_ASIGNACION">Nueva Asignación de Código QR</option>
            <option value="CORRECCION">Corrección por Mal Levantamiento</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Motivo u Observaciones</label>
          <textarea
            :value="form.motivo"
            @input="updateFormField('motivo', $event.target.value)"
            rows="3"
            placeholder="Describe brevemente el motivo u observaciones adicionales..."
            class="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-900/30 text-sm font-medium text-slate-900"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Botones de Navegación y Envío Final -->
    <div class="flex justify-between items-center pt-4 border-t border-slate-100">
      <button
        type="button"
        @click="$emit('prev-step')"
        class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm rounded-xl transition cursor-pointer"
      >
        ← Anterior
      </button>
      <button
        type="submit"
        :disabled="submitting || !selectedPlantel"
        class="px-8 py-3.5 bg-blue-900 hover:bg-blue-950 disabled:bg-slate-300 text-white font-extrabold text-base rounded-2xl transition shadow-lg shadow-blue-900/20 flex items-center justify-center space-x-2 cursor-pointer"
      >
        <span v-if="submitting">Procesando Solicitud...</span>
        <span v-else>Enviar Solicitud de Código QR</span>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  form: {
    type: Object,
    required: true
  },
  selectedPlantel: Object,
  submitting: Boolean
})

const emit = defineEmits(['update:form', 'prev-step'])

function updateFormField(key, val) {
  emit('update:form', {
    ...props.form,
    [key]: val
  })
}
</script>
