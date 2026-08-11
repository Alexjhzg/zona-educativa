<template>
  <div class="w-full max-w-2xl mx-auto bg-white rounded-3xl shadow-xl shadow-slate-200/60 border border-slate-100 p-6 md:p-10">
    <!-- Header del Formulario -->
    <div class="flex items-center space-x-3.5 mb-6 pb-6 border-b border-slate-100">
      <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-900 to-slate-900 text-white flex items-center justify-center font-extrabold text-xl shadow-md shadow-blue-900/20">
        QR
      </div>
      <div>
        <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight font-heading">
          Solicitud de Código QR
        </h2>
        <p class="text-xs md:text-sm text-slate-500 font-medium mt-0.5">
          Paso {{ currentStep }} de 4: {{ getStepTitle(currentStep) }}
        </p>
      </div>
    </div>

    <!-- Stepper de Progreso -->
    <WizardStepper
      v-if="!submittedSuccess"
      :current-step="currentStep"
      @go-to-step="goToStep"
    />

    <!-- Pantalla de Éxito al Enviar -->
    <div v-if="submittedSuccess" class="bg-emerald-50 border border-emerald-200 rounded-2xl p-6 text-emerald-900 text-center animate-fade-in space-y-3">
      <div class="w-12 h-12 bg-emerald-500 text-white rounded-full flex items-center justify-center mx-auto shadow-sm">
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
        </svg>
      </div>
      <h3 class="text-lg font-extrabold font-heading text-slate-900">¡Solicitud Registrada Exitosamente!</h3>
      <p class="text-sm text-emerald-800">
        Hemos registrado tu solicitud para el plantel <strong>{{ selectedPlantel?.plantel }}</strong> (Código DEA: {{ selectedPlantel?.codigo_dea }}).
      </p>
      <button 
        @click="resetForm" 
        class="inline-flex items-center justify-center px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl transition shadow-md shadow-emerald-200 cursor-pointer"
      >
        Realizar Otra Solicitud
      </button>
    </div>

    <!-- Formulario Multi-Paso (Wizard Modolarizado) -->
    <form v-else @submit.prevent="handleSubmit">
      
      <!-- Paso 1: Rol -->
      <StepRolSelection
        v-if="currentStep === 1"
        v-model="form.solicitante_rol"
        @next-step="nextStep"
      />

      <!-- Paso 2: Búsqueda del Plantel -->
      <StepPlantelSearch
        v-if="currentStep === 2"
        :dea-input="deaInput"
        :ci-input="ciInput"
        :active-search-source="activeSearchSource"
        :selected-plantel="selectedPlantel"
        :search-results="searchResults"
        :loading-search="loadingSearch"
        :solicitante-rol="form.solicitante_rol"
        :show-director-update-form="showDirectorUpdateForm"
        v-model:nuevo-director="nuevoDirector"
        @on-dea-input="handleDeaInput"
        @on-ci-input="handleCiInput"
        @select-plantel="handleSelectPlantel"
        @clear-plantel="clearPlantel"
        @open-director-update="openDirectorUpdateForm"
        @cancel-director-update="cancelDirectorUpdate"
        @prev-step="prevStep"
        @next-step="nextStep"
      />

      <!-- Paso 3: Contacto -->
      <StepContactDetails
        v-if="currentStep === 3"
        v-model:form="form"
        :show-director-update-form="showDirectorUpdateForm"
        @cancel-director-update="cancelDirectorUpdate"
        @prev-step="prevStep"
        @next-step="nextStep"
      />

      <!-- Paso 4: Detalles y Envío -->
      <StepRequestDetails
        v-if="currentStep === 4"
        v-model:form="form"
        :selected-plantel="selectedPlantel"
        :submitting="submitting"
        @prev-step="prevStep"
      />

    </form>
  </div>
</template>

<script setup>
import { useSolicitudForm } from '../composables/useSolicitudForm'

import WizardStepper from './wizard/WizardStepper.vue'
import StepRolSelection from './wizard/StepRolSelection.vue'
import StepPlantelSearch from './wizard/StepPlantelSearch.vue'
import StepContactDetails from './wizard/StepContactDetails.vue'
import StepRequestDetails from './wizard/StepRequestDetails.vue'

const {
  currentStep,
  deaInput,
  ciInput,
  selectedPlantel,
  submitting,
  submittedSuccess,
  activeSearchSource,
  showDirectorUpdateForm,
  nuevoDirector,
  form,
  searchResults,
  loadingSearch,
  getStepTitle,
  nextStep,
  prevStep,
  goToStep,
  handleDeaInput,
  handleCiInput,
  handleSelectPlantel,
  clearPlantel,
  openDirectorUpdateForm,
  cancelDirectorUpdate,
  handleSubmit,
  resetForm,
  formatCiDisplay
} = useSolicitudForm()
</script>
