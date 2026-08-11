<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <div class="flex justify-between items-center mb-3">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-blue-900 text-white font-extrabold text-xs flex items-center justify-center shadow-xs">3</span>
          <label class="block text-base font-extrabold text-slate-900">
            Datos de Contacto del Solicitante <span class="text-red-500">*</span>
          </label>
        </div>
        <span v-if="form.solicitante_rol === 'DIRECTOR' && showDirectorUpdateForm" class="inline-flex items-center text-[11px] font-bold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-md border border-amber-200">
          <svg class="w-3.5 h-3.5 text-amber-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
          Actualización de Datos Solicitada
        </span>
        <span v-else-if="form.solicitante_rol === 'DIRECTOR'" class="inline-flex items-center text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-200">
          <svg class="w-3.5 h-3.5 text-emerald-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          Datos Protegidos (Verificados en BD)
        </span>
      </div>

      <!-- Banner Informativo: Solicitud de Actualización de Datos del Director -->
      <div v-if="form.solicitante_rol === 'DIRECTOR' && showDirectorUpdateForm" class="mb-4 p-4 bg-gradient-to-r from-amber-50 to-orange-50/80 border border-amber-200/90 rounded-2xl shadow-xs space-y-1.5 animate-fade-in">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2 text-amber-900 font-extrabold text-xs md:text-sm">
            <svg class="w-4 h-4 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            <span>Solicitud de Actualización de Datos del Director</span>
          </div>
          <button 
            @click="$emit('cancel-director-update')" 
            type="button"
            class="text-xs font-bold text-amber-800 hover:text-amber-950 underline cursor-pointer shrink-0 ml-2"
          >
            Restablecer datos en BD ✕
          </button>
        </div>
        <p class="text-xs text-amber-800/90 font-medium">
          Los campos a continuación contienen la nueva información ingresada.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-50/70 p-4 border border-slate-200/80 rounded-2xl">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">
            {{ form.solicitante_rol === 'REPRESENTANTE' ? 'Nombre del Representante' : 'Nombre del Director' }}
          </label>
          <input
            :value="form.solicitante_nombre"
            @input="updateFormField('solicitante_nombre', $event.target.value, cleanNombre)"
            type="text"
            :readonly="form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm"
            :placeholder="form.solicitante_rol === 'REPRESENTANTE' ? 'Ej. Juan Pérez' : 'Nombre completo'"
            :class="[
              form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm
                ? 'bg-slate-100/90 border-slate-200 text-slate-700 cursor-not-allowed select-none'
                : 'bg-white border-slate-200 text-slate-900 focus:ring-2 focus:ring-blue-900/30'
            ]"
            class="w-full px-4 py-2.5 rounded-xl border text-sm font-medium focus:outline-none transition"
            required
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">
            {{ form.solicitante_rol === 'REPRESENTANTE' ? 'Cédula del Representante' : 'Cédula de Identidad' }}
          </label>
          <input
            :value="form.solicitante_ci"
            @input="updateFormField('solicitante_ci', $event.target.value, cleanCi)"
            type="text"
            :readonly="form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm"
            placeholder="Ej. V-12345678"
            :class="[
              form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm
                ? 'bg-slate-100/90 border-slate-200 text-slate-700 cursor-not-allowed select-none'
                : 'bg-white border-slate-200 text-slate-900 focus:ring-2 focus:ring-blue-900/30'
            ]"
            class="w-full px-4 py-2.5 rounded-xl border text-sm font-medium focus:outline-none transition"
            required
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Teléfono de Contacto</label>
          <input
            :value="form.solicitante_telefono"
            @input="updateFormField('solicitante_telefono', $event.target.value, cleanTelefono)"
            type="tel"
            :readonly="form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm"
            placeholder="Ej. 0414-1234567"
            :class="[
              form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm
                ? 'bg-slate-100/90 border-slate-200 text-slate-700 cursor-not-allowed select-none'
                : 'bg-white border-slate-200 text-slate-900 focus:ring-2 focus:ring-blue-900/30'
            ]"
            class="w-full px-4 py-2.5 rounded-xl border text-sm font-medium focus:outline-none transition"
            required
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Correo Electrónico</label>
          <input
            :value="form.solicitante_email"
            @input="updateFormField('solicitante_email', $event.target.value, val => val)"
            type="email"
            :readonly="form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm"
            placeholder="ejemplo@educacion.gob.ve"
            :class="[
              form.solicitante_rol === 'DIRECTOR' && !showDirectorUpdateForm
                ? 'bg-slate-100/90 border-slate-200 text-slate-700 cursor-not-allowed select-none'
                : 'bg-white border-slate-200 text-slate-900 focus:ring-2 focus:ring-blue-900/30'
            ]"
            class="w-full px-4 py-2.5 rounded-xl border text-sm font-medium focus:outline-none transition"
            required
          />
        </div>
      </div>
    </div>

    <!-- Botones de Navegación Paso 3 -->
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
        class="px-6 py-3 bg-blue-900 hover:bg-blue-950 text-white font-bold text-sm rounded-xl transition shadow-md shadow-blue-900/10 inline-flex items-center space-x-2 cursor-pointer"
      >
        <span>Siguiente: Detalles y Envío</span>
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
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
  showDirectorUpdateForm: Boolean
})

const emit = defineEmits(['update:form', 'cancel-director-update', 'prev-step', 'next-step'])

function cleanNombre(val) {
  return String(val || '').replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '')
}

function cleanCi(val) {
  return String(val || '').replace(/[^0-9veVE-]/g, '').toUpperCase()
}

function cleanTelefono(val) {
  return String(val || '').replace(/[^0-9-\s]/g, '')
}

function updateFormField(key, rawValue, cleanerFn) {
  const cleaned = cleanerFn(rawValue)
  emit('update:form', {
    ...props.form,
    [key]: cleaned
  })
}
</script>
