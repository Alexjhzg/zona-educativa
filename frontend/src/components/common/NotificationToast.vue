<template>
  <div class="fixed top-5 right-5 z-50 flex flex-col space-y-3 max-w-sm w-full pointer-events-none">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'pointer-events-auto p-4 rounded-2xl shadow-xl border backdrop-blur-md flex items-start space-x-3 transition-all duration-300 transform',
          toast.type === 'success' ? 'bg-emerald-900/90 border-emerald-500/50 text-white' :
          toast.type === 'error' ? 'bg-rose-900/90 border-rose-500/50 text-white' :
          toast.type === 'warning' ? 'bg-amber-900/90 border-amber-500/50 text-white' :
          'bg-slate-900/90 border-slate-700 text-white'
        ]"
      >
        <!-- Iconos SVG estandarizados -->
        <div class="shrink-0 pt-0.5">
          <svg v-if="toast.type === 'success'" class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <svg v-else class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>

        <div class="flex-grow text-xs font-medium leading-relaxed">
          <p v-if="toast.title" class="font-extrabold text-sm mb-0.5 tracking-wide">{{ toast.title }}</p>
          <p>{{ toast.message }}</p>
        </div>

        <button @click="removeToast(toast.id)" class="shrink-0 text-white/60 hover:text-white transition p-0.5 cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let nextId = 1

function addToast({ title = '', message = '', type = 'info', duration = 3500 }) {
  const id = nextId++
  toasts.value.push({ id, title, message, type })

  if (duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }
}

function removeToast(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

defineExpose({
  addToast,
  success(message, title = 'Éxito') {
    addToast({ title, message, type: 'success' })
  },
  error(message, title = 'Error') {
    addToast({ title, message, type: 'error' })
  },
  info(message, title = 'Información') {
    addToast({ title, message, type: 'info' })
  },
  warning(message, title = 'Advertencia') {
    addToast({ title, message, type: 'warning' })
  }
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
</style>
