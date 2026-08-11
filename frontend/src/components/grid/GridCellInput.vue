<template>
  <td
    @click="$emit('focus-cell')"
    @dblclick="$emit('start-edit')"
    :class="[
      isEditing
        ? 'ring-2 ring-blue-600 bg-white p-0 z-20'
        : isFocused
          ? 'ring-2 ring-blue-500 bg-blue-50/80 font-bold z-10'
          : 'hover:bg-amber-50/80 cursor-pointer',
      isSaved ? 'bg-emerald-100 transition-colors duration-500' : ''
    ]"
    class="py-2.5 px-3 border-r border-slate-200/80 font-medium whitespace-nowrap relative min-w-[120px]"
  >
    <!-- Campo de selección desplegable (<select>) -->
    <select
      v-if="isEditing && col.type === 'select'"
      :value="editingVal"
      @input="$emit('update:editingVal', $event.target.value)"
      @change="$emit('save-cell')"
      @keyup.esc="$emit('cancel-edit')"
      ref="inputRef"
      class="w-full h-full px-2 py-1 bg-white font-semibold text-xs text-blue-950 border-none outline-none focus:ring-0 cursor-pointer"
    >
      <option v-for="opt in col.options" :key="opt" :value="opt">
        {{ opt }}
      </option>
    </select>

    <!-- Campo de entrada libre (<input>) -->
    <input
      v-else-if="isEditing"
      :value="editingVal"
      @input="$emit('update:editingVal', $event.target.value)"
      @blur="$emit('save-cell')"
      @keyup.enter="$emit('save-cell')"
      @keyup.esc="$emit('cancel-edit')"
      ref="inputRef"
      type="text"
      class="w-full h-full px-2 py-1 bg-white font-medium text-xs text-slate-900 border-none outline-none focus:ring-0"
    />

    <!-- Render de valor en lectura -->
    <span v-else class="flex items-center justify-between">
      <span>{{ cellValue !== null && cellValue !== undefined ? cellValue : '-' }}</span>
      <span v-if="col.type === 'select'" class="text-[9px] text-slate-400 group-hover:text-blue-600 transition">
        ▼
      </span>
    </span>
  </td>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  cellValue: [String, Number, Object],
  col: {
    type: Object,
    required: true
  },
  isEditing: Boolean,
  isFocused: Boolean,
  isSaved: Boolean,
  editingVal: [String, Number]
})

defineEmits(['focus-cell', 'start-edit', 'save-cell', 'cancel-edit', 'update:editingVal'])

const inputRef = ref(null)

watch(() => props.isEditing, (newVal) => {
  if (newVal) {
    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus()
      }
    })
  }
})
</script>
