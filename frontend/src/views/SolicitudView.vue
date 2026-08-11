<template>
  <div class="min-h-screen bg-[#F8FAFC] flex flex-col justify-between py-8 px-4 sm:px-6">
    <!-- Banner Institucional Superior -->
    <header class="max-w-4xl mx-auto w-full mb-6 text-center">
      <div class="inline-flex items-center justify-center space-x-2 px-3.5 py-1.5 bg-blue-50 border border-blue-100 rounded-full text-blue-900 font-bold text-xs mb-3 shadow-xs">
        <span>Ministerio del Poder Popular para la Educación</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight font-heading">
        Zona Educativa del Estado Monagas
      </h1>
      <p class="text-slate-500 font-medium text-sm md:text-base max-w-xl mx-auto mt-1">
        Formulario Oficial para la Solicitud, Reposición y Asignación de Códigos QR en Planteles Educativos.
      </p>
    </header>

    <!-- Componente Formulario Público -->
    <main class="flex-grow flex items-center justify-center my-4">
      <FormSolicitud />
    </main>

    <!-- Footer Discreto -->
    <footer class="max-w-4xl mx-auto w-full text-center mt-8 pt-4 border-t border-slate-200/60 text-xs text-slate-400">
      <p>© 2026 Zona Educativa - Todos los derechos reservados.</p>
      <div class="mt-2">
        <router-link to="/admin/login" class="text-slate-400 hover:text-blue-900 font-medium transition underline">
          Acceso Personal Administrativo (Zona Educativa)
        </router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import FormSolicitud from '../components/FormSolicitud.vue'
</script>
