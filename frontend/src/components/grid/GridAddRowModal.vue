<template>
  <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-fade-in">
    <div class="bg-white rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-100">
      <div class="flex justify-between items-center border-b border-slate-100 pb-3">
        <h3 class="text-base font-extrabold text-slate-900 font-heading">
          Agregar Registro a Tabla: {{ activeTable }}
        </h3>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-700 font-bold p-1 cursor-pointer">
          ✕
        </button>
      </div>

      <form @submit.prevent="$emit('save-new-row')" class="space-y-3 text-xs">
        <div v-for="col in columns.filter(c => c.key !== 'id')" :key="col.key">
          <label class="block font-semibold text-slate-700 mb-1">{{ col.label }}</label>
          
          <select
            v-if="col.type === 'select'"
            :value="newRowForm[col.key]"
            @change="updateField(col.key, $event.target.value)"
            class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:ring-2 focus:ring-blue-900/20"
            required
          >
            <option value="">Seleccione una opción</option>
            <option v-for="opt in col.options" :key="opt" :value="opt">{{ opt }}</option>
          </select>

          <input
            v-else
            :value="newRowForm[col.key]"
            @input="updateField(col.key, $event.target.value)"
            type="text"
            :placeholder="col.label"
            class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:ring-2 focus:ring-blue-900/20"
            required
          />
        </div>

        <div class="flex justify-end space-x-2 pt-3 border-t border-slate-100">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl transition cursor-pointer"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="savingNewRow"
            class="px-5 py-2 bg-blue-900 hover:bg-blue-950 text-white font-extrabold rounded-xl transition shadow-md shadow-blue-900/10 cursor-pointer"
          >
            <span>{{ savingNewRow ? 'Guardando...' : 'Crear Registro' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  activeTable: String,
  columns: Array,
  newRowForm: Object,
  savingNewRow: Boolean
})

const emit = defineEmits(['close', 'save-new-row', 'update:newRowForm'])

function updateField(key, value) {
  emit('update:newRowForm', {
    ...props.newRowForm,
    [key]: value
  })
}
</script>
