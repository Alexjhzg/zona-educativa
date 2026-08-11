import { ref, watchEffect } from 'vue'

const savedTheme = localStorage.getItem('app_theme') || 'dark'
const isDark = ref(savedTheme === 'dark')

watchEffect(() => {
  localStorage.setItem('app_theme', isDark.value ? 'dark' : 'light')
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    document.documentElement.classList.remove('light')
  } else {
    document.documentElement.classList.add('light')
    document.documentElement.classList.remove('dark')
  }
})

export function useTheme() {
  function toggleTheme() {
    isDark.value = !isDark.value
  }

  return {
    isDark,
    toggleTheme
  }
}
