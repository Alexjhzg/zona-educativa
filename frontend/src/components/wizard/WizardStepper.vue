<template>
  <div class="mb-8">
    <div class="flex items-center justify-between relative">
      <!-- Línea de Fondo Base -->
      <div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1.5 bg-slate-200/70 rounded-full -z-0"></div>
      
      <!-- Línea de Progreso Animada con Gradiente -->
      <div 
        class="absolute left-0 top-1/2 transform -translate-y-1/2 h-1.5 bg-gradient-to-r from-emerald-600 to-blue-900 rounded-full transition-all duration-500 ease-out -z-0 shadow-xs"
        :style="{ width: ((currentStep - 1) / 3) * 100 + '%' }"
      ></div>

      <!-- Nodos de Pasos -->
      <div 
        v-for="step in 4" 
        :key="step"
        @click="$emit('go-to-step', step)"
        :class="[
          currentStep === step 
            ? 'bg-gradient-to-br from-blue-900 to-indigo-950 text-white ring-4 ring-blue-500/20 font-black scale-110 shadow-md' 
            : step < currentStep 
              ? 'bg-emerald-600 text-white font-extrabold cursor-pointer hover:bg-emerald-700 shadow-xs' 
              : 'bg-white border-2 border-slate-300 text-slate-400 font-bold'
        ]"
        class="w-9 h-9 rounded-2xl flex items-center justify-center text-xs relative z-10 transition-all duration-300 cursor-pointer"
      >
        <svg v-if="step < currentStep" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
        </svg>
        <span v-else>{{ step }}</span>
      </div>
    </div>
    
    <!-- Etiquetas de Pasos -->
    <div class="flex justify-between text-[11px] font-extrabold text-slate-400 mt-2.5 px-0.5 uppercase tracking-wider">
      <span :class="{ 'text-blue-900 font-black scale-105': currentStep === 1 }">1. Rol</span>
      <span :class="{ 'text-blue-900 font-black scale-105': currentStep === 2 }">2. Plantel</span>
      <span :class="{ 'text-blue-900 font-black scale-105': currentStep === 3 }">3. Contacto</span>
      <span :class="{ 'text-blue-900 font-black scale-105': currentStep === 4 }">4. Detalles</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  currentStep: {
    type: Number,
    required: true
  }
})

defineEmits(['go-to-step'])
</script>
