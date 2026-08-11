import { ref, reactive, computed, watch } from 'vue'
import { usePlantelesStore } from '../stores/planteles'
import { useSolicitudesStore } from '../stores/solicitudes'
import { toast } from 'vue3-toastify'

export function useSolicitudForm() {
  const plantelesStore = usePlantelesStore()
  const solicitudesStore = useSolicitudesStore()

  const currentStep = ref(1)
  const deaInput = ref('')
  const ciInput = ref('')
  const selectedPlantel = ref(null)
  const submitting = ref(false)
  const submittedSuccess = ref(false)
  const activeSearchSource = ref('dea')
  const showDirectorUpdateForm = ref(false)

  const nuevoDirector = reactive({
    nombre: '',
    ci: '',
    telefono: '',
    email: ''
  })

  const form = reactive({
    solicitante_rol: '',
    tipo_solicitud: 'REPOSICION',
    solicitante_nombre: '',
    solicitante_ci: '',
    solicitante_telefono: '',
    solicitante_email: '',
    motivo: ''
  })

  const searchResults = computed(() => plantelesStore.searchResults)
  const loadingSearch = computed(() => plantelesStore.loadingSearch)

  function getStepTitle(step) {
    if (step === 1) return '¿Quién realiza la solicitud?'
    if (step === 2) return 'Identificación y Búsqueda del Plantel'
    if (step === 3) return 'Datos de Contacto del Solicitante'
    if (step === 4) return 'Detalles y Envío de la Solicitud'
    return ''
  }

  function nextStep() {
    if (currentStep.value === 1) {
      if (!form.solicitante_rol) {
        toast.warning('Por favor selecciona quién realiza la solicitud para continuar.')
        return
      }
      currentStep.value = 2
    } else if (currentStep.value === 2) {
      if (!selectedPlantel.value) {
        toast.warning('Por favor busca y selecciona un plantel antes de continuar.')
        return
      }
      currentStep.value = 3
    } else if (currentStep.value === 3) {
      if (!form.solicitante_nombre || !form.solicitante_ci) {
        toast.warning('Por favor completa los datos de contacto.')
        return
      }
      currentStep.value = 4
    }
  }

  function prevStep() {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  function goToStep(step) {
    if (step < currentStep.value) {
      currentStep.value = step
    } else if (step === 2 && form.solicitante_rol) {
      currentStep.value = 2
    } else if (step === 3 && selectedPlantel.value) {
      currentStep.value = 3
    } else if (step === 4 && selectedPlantel.value && form.solicitante_nombre) {
      currentStep.value = 4
    }
  }

  function cleanDeaInput(val) {
    return String(val || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase()
  }

  function cleanCiInput(val) {
    return String(val || '').replace(/[^0-9veVE-]/g, '').toUpperCase()
  }

  function formatCiDisplay(ciVal) {
    if (!ciVal) return ''
    return String(ciVal).replace('.0', '').trim()
  }

  let searchTimeout = null

  function handleDeaInput(rawVal) {
    activeSearchSource.value = 'dea'
    ciInput.value = ''
    deaInput.value = cleanDeaInput(rawVal)
    clearTimeout(searchTimeout)
    const val = deaInput.value.trim()
    if (!val) {
      selectedPlantel.value = null
      plantelesStore.searchResults = []
      return
    }

    searchTimeout = setTimeout(async () => {
      const exactMatch = await plantelesStore.buscarPorCodigoDEA(val)
      if (exactMatch) {
        handleSelectPlantel(exactMatch, 'dea')
      } else {
        plantelesStore.buscarPlanteles(val)
      }
    }, 250)
  }

  function handleCiInput(rawVal) {
    activeSearchSource.value = 'ci'
    deaInput.value = ''
    ciInput.value = cleanCiInput(rawVal)
    clearTimeout(searchTimeout)
    const val = ciInput.value.trim()
    if (!val) {
      selectedPlantel.value = null
      plantelesStore.searchResults = []
      return
    }

    searchTimeout = setTimeout(async () => {
      const exactMatch = await plantelesStore.buscarPorCodigoDEA(val)
      if (exactMatch) {
        handleSelectPlantel(exactMatch, 'ci')
      } else {
        plantelesStore.buscarPlanteles(val)
      }
    }, 250)
  }

  function autoFillDirectorData(item) {
    if (item.nombres_contacto) form.solicitante_nombre = item.nombres_contacto
    if (item.ci_contacto) form.solicitante_ci = formatCiDisplay(item.ci_contacto)
    if (item.telefono_contacto) form.solicitante_telefono = String(item.telefono_contacto).replace('.0', '')
    if (item.email_contacto) form.solicitante_email = item.email_contacto
  }

  function handleSelectPlantel(item, source = activeSearchSource.value) {
    selectedPlantel.value = item
    if (source === 'dea') {
      deaInput.value = item.codigo_dea
      ciInput.value = ''
    } else {
      ciInput.value = formatCiDisplay(item.ci_contacto)
      deaInput.value = ''
    }
    plantelesStore.searchResults = []
    showDirectorUpdateForm.value = false

    if (form.solicitante_rol === 'DIRECTOR') {
      autoFillDirectorData(item)
    }
  }

  function clearPlantel() {
    selectedPlantel.value = null
    deaInput.value = ''
    ciInput.value = ''
    activeSearchSource.value = ''
    showDirectorUpdateForm.value = false
    plantelesStore.searchResults = []
  }

  function openDirectorUpdateForm() {
    showDirectorUpdateForm.value = true
    if (selectedPlantel.value && form.solicitante_rol === 'DIRECTOR') {
      if (!nuevoDirector.nombre) nuevoDirector.nombre = selectedPlantel.value.nombres_contacto || ''
      if (!nuevoDirector.ci) nuevoDirector.ci = formatCiDisplay(selectedPlantel.value.ci_contacto) || ''
      if (!nuevoDirector.telefono) nuevoDirector.telefono = String(selectedPlantel.value.telefono_contacto || '').replace('.0', '')
      if (!nuevoDirector.email) nuevoDirector.email = selectedPlantel.value.email_contacto || ''

      form.solicitante_nombre = nuevoDirector.nombre
      form.solicitante_ci = nuevoDirector.ci
      form.solicitante_telefono = nuevoDirector.telefono
      form.solicitante_email = nuevoDirector.email
    }
  }

  function cancelDirectorUpdate() {
    showDirectorUpdateForm.value = false
    nuevoDirector.nombre = ''
    nuevoDirector.ci = ''
    nuevoDirector.telefono = ''
    nuevoDirector.email = ''
    if (selectedPlantel.value && form.solicitante_rol === 'DIRECTOR') {
      autoFillDirectorData(selectedPlantel.value)
    }
  }

  watch(() => form.solicitante_rol, (newRol) => {
    if (newRol === 'REPRESENTANTE') {
      form.solicitante_nombre = ''
      form.solicitante_ci = ''
      form.solicitante_telefono = ''
      form.solicitante_email = ''
    } else if (newRol === 'DIRECTOR' && selectedPlantel.value && !showDirectorUpdateForm.value) {
      autoFillDirectorData(selectedPlantel.value)
    }
  })

  watch(nuevoDirector, (newVal) => {
    if (showDirectorUpdateForm.value && form.solicitante_rol === 'DIRECTOR') {
      form.solicitante_nombre = newVal.nombre
      form.solicitante_ci = newVal.ci
      form.solicitante_telefono = newVal.telefono
      form.solicitante_email = newVal.email
    }
  }, { deep: true })

  async function handleSubmit() {
    if (!selectedPlantel.value) return
    submitting.value = true

    if (showDirectorUpdateForm.value && form.solicitante_rol === 'DIRECTOR') {
      form.solicitante_nombre = nuevoDirector.nombre
      form.solicitante_ci = nuevoDirector.ci
      form.solicitante_telefono = nuevoDirector.telefono
      form.solicitante_email = nuevoDirector.email
    }

    try {
      let observacionFinal = form.motivo || ''
      if (showDirectorUpdateForm.value) {
        observacionFinal = `[SOLICITUD CAMBIO DIRECTOR - Corroborar datos registrados vs nuevos datos: ${nuevoDirector.nombre}, CI: ${nuevoDirector.ci}] | ` + observacionFinal
      }

      const payload = {
        plantel_id: selectedPlantel.value.id,
        tipo_solicitud: form.tipo_solicitud,
        solicitante_rol: form.solicitante_rol,
        solicitante_nombre: form.solicitante_nombre,
        solicitante_ci: form.solicitante_ci,
        solicitante_telefono: form.solicitante_telefono,
        solicitante_email: form.solicitante_email,
        motivo: observacionFinal
      }

      await solicitudesStore.enviarSolicitudQR(payload)
      submittedSuccess.value = true
    } catch (err) {
      toast.error('Error al enviar la solicitud. Por favor verifique los datos.')
      console.error(err)
    } finally {
      submitting.value = false
    }
  }

  function resetForm() {
    currentStep.value = 1
    submittedSuccess.value = false
    selectedPlantel.value = null
    deaInput.value = ''
    ciInput.value = ''
    activeSearchSource.value = ''
    showDirectorUpdateForm.value = false
    nuevoDirector.nombre = ''
    nuevoDirector.ci = ''
    nuevoDirector.telefono = ''
    nuevoDirector.email = ''
    form.solicitante_rol = ''
    form.solicitante_nombre = ''
    form.solicitante_ci = ''
    form.solicitante_telefono = ''
    form.solicitante_email = ''
    form.motivo = ''
  }

  return {
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
  }
}
