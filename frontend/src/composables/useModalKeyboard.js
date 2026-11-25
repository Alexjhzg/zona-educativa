import { ref, watch, onUnmounted } from 'vue'

export function useModalKeyboard(isOpen, { onLeft, onRight, onEscape }) {
  const handleKeydown = (e) => {
    // No navegar si el foco está en un input/textarea
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return

    if (e.key === 'ArrowLeft') {
      e.preventDefault()
      if (onLeft) onLeft()
    }
    if (e.key === 'ArrowRight') {
      e.preventDefault()
      if (onRight) onRight()
    }
    if (e.key === 'Escape') {
      e.preventDefault()
      if (onEscape) onEscape()
    }
  }

  // Registrar/desregistrar listener según estado del modal
  watch(
    () => (typeof isOpen === 'function' ? isOpen() : isOpen.value),
    (open) => {
      if (open) {
        window.addEventListener('keydown', handleKeydown)
      } else {
        window.removeEventListener('keydown', handleKeydown)
      }
    },
    { immediate: true }
  )

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
  })
}
