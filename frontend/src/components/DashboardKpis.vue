<template>
  <div v-if="kpis" class="space-y-6 animate-fade-in">
    <!-- 1. Tarjetas Superiores de Métricas (KPI Cards - Sapphire Glass Style) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white/90 backdrop-blur-xl p-5 rounded-3xl border border-slate-200/80 shadow-lg shadow-blue-950/5 hover:border-blue-900/40 transition-all duration-300 flex items-center justify-between group">
        <div>
          <span class="text-[11px] font-extrabold text-slate-400 uppercase tracking-wider block">Total Planteles</span>
          <div class="text-3xl md:text-4xl font-black text-slate-900 font-heading mt-1 group-hover:scale-105 transition-transform duration-200">
            {{ kpis.total_planteles }}
          </div>
          <span class="text-[10px] text-blue-900 font-bold bg-blue-50 px-2 py-0.5 rounded-md mt-2 inline-block">Monagas</span>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-blue-900 text-white flex items-center justify-center font-bold shadow-md shadow-blue-900/20 group-hover:rotate-6 transition-transform">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0h4m-4 0V11m0 0h4m-4 0H7m4 0v10"/>
          </svg>
        </div>
      </div>

      <div class="bg-white/90 backdrop-blur-xl p-5 rounded-3xl border border-emerald-200/80 shadow-lg shadow-emerald-950/5 hover:border-emerald-500/40 transition-all duration-300 flex items-center justify-between group">
        <div>
          <span class="text-[11px] font-extrabold text-emerald-700 uppercase tracking-wider block">QR Asignados SEGEN</span>
          <div class="text-3xl md:text-4xl font-black text-slate-900 font-heading mt-1 group-hover:scale-105 transition-transform duration-200">
            {{ kpis.total_qr_segen }}
          </div>
          <span class="text-[10px] text-emerald-700 font-extrabold bg-emerald-50 px-2 py-0.5 rounded-md mt-2 inline-block">
            {{ ((kpis.total_qr_segen / (kpis.total_planteles || 1)) * 100).toFixed(1) }}% Cobertura
          </span>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center font-bold shadow-md shadow-emerald-600/20 group-hover:rotate-6 transition-transform">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
      </div>

      <div class="bg-white/90 backdrop-blur-xl p-5 rounded-3xl border border-slate-200/80 shadow-lg shadow-slate-950/5 hover:border-slate-400/40 transition-all duration-300 flex items-center justify-between group">
        <div>
          <span class="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider block">Sin QR Asignado</span>
          <div class="text-3xl md:text-4xl font-black text-slate-900 font-heading mt-1 group-hover:scale-105 transition-transform duration-200">
            {{ kpis.total_sin_qr }}
          </div>
          <span class="text-[10px] text-slate-600 font-bold bg-slate-100 px-2 py-0.5 rounded-md mt-2 inline-block">Pendientes</span>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-slate-800 text-white flex items-center justify-center font-bold shadow-md shadow-slate-800/20 group-hover:rotate-6 transition-transform">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
      </div>

      <div class="bg-white/90 backdrop-blur-xl p-5 rounded-3xl border border-amber-200/80 shadow-lg shadow-amber-950/5 hover:border-amber-500/40 transition-all duration-300 flex items-center justify-between group">
        <div>
          <span class="text-[11px] font-extrabold text-amber-700 uppercase tracking-wider block">Reponer QR</span>
          <div class="text-3xl md:text-4xl font-black text-slate-900 font-heading mt-1 group-hover:scale-105 transition-transform duration-200">
            {{ kpis.total_reponer_qr }}
          </div>
          <span class="text-[10px] text-amber-800 font-bold bg-amber-50 px-2 py-0.5 rounded-md mt-2 inline-block">Deterioro / Pérdida</span>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-amber-600 text-white flex items-center justify-center font-bold shadow-md shadow-amber-600/20 group-hover:rotate-6 transition-transform">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 2. Bento Grid Central Estilo Stitch Sapphire Glass -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Tarjeta Principal de Demanda por Rol -->
      <div class="lg:col-span-2 bg-gradient-to-br from-blue-950 via-blue-900 to-indigo-950 text-white rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden flex flex-col justify-between border border-blue-800/50">
        <!-- Glow ambiental de Stitch -->
        <div class="absolute -right-16 -top-16 w-80 h-80 bg-cyan-400/20 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -left-16 -bottom-16 w-80 h-80 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="relative z-10">
          <div class="flex flex-col sm:flex-row justify-between sm:items-start gap-4 mb-6">
            <div>
              <span class="inline-flex items-center space-x-1.5 px-3 py-1 bg-cyan-400/15 text-cyan-300 rounded-full text-[11px] font-extrabold uppercase tracking-wider mb-2 border border-cyan-400/30">
                <svg class="w-3.5 h-3.5 text-cyan-300 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
                Indicador Clave de Demanda
              </span>
              <h3 class="text-2xl md:text-3xl font-black font-heading text-white tracking-tight">
                ¿Quién solicita mayormente cantidad de QR?
              </h3>
              <p class="text-xs text-blue-200 mt-1">
                Análisis porcentual por rol institucional basado en las solicitudes procesadas.
              </p>
            </div>
            <div class="bg-white/10 backdrop-blur-md px-4 py-2 rounded-2xl text-xs font-black text-cyan-300 border border-white/15 self-start shrink-0">
              Rol Líder: {{ kpis.top_solicitante_rol || 'DIRECTOR' }}
            </div>
          </div>

          <!-- Progress Bars por Rol -->
          <div class="space-y-4 my-6">
            <div v-for="item in kpis.ranking_roles" :key="item.rol" class="space-y-1.5">
              <div class="flex justify-between text-xs font-bold">
                <span class="text-blue-100 flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-xs"></span>
                  <span>{{ formatRolName(item.rol) }}</span>
                </span>
                <span class="text-cyan-300 font-mono font-bold">{{ item.total_solicitudes }} solicitudes ({{ item.porcentaje }}%)</span>
              </div>
              <div class="w-full h-3.5 bg-white/10 rounded-full overflow-hidden p-0.5 backdrop-blur-md border border-white/10">
                <div 
                  class="h-full bg-gradient-to-r from-cyan-400 via-teal-400 to-emerald-400 rounded-full transition-all duration-1000 ease-out shadow-md"
                  :style="{ width: item.porcentaje + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-white/15 flex flex-col sm:flex-row justify-between sm:items-center text-xs text-blue-200 gap-2 relative z-10">
          <span>Total Solicitudes Registradas: <strong class="text-white font-mono font-bold">{{ kpis.total_solicitudes_registradas }}</strong></span>
          <span class="text-emerald-400 font-extrabold inline-flex items-center space-x-1">
            <svg class="w-4 h-4 text-emerald-400 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
            </svg>
            <span>Sincronizado con PostgreSQL</span>
          </span>
        </div>
      </div>

      <!-- Resumen por Municipio -->
      <div class="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-slate-200/80 shadow-lg shadow-slate-950/5 flex flex-col justify-between space-y-4">
        <div>
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-black text-slate-900 font-heading">
              Planteles por Municipio
            </h4>
            <span class="text-[10px] font-extrabold text-blue-900 bg-blue-50 px-2.5 py-1 rounded-xl border border-blue-100 uppercase">
              Monagas
            </span>
          </div>
          
          <div class="space-y-2.5 max-h-[320px] overflow-y-auto pr-1">
            <div v-for="mun in kpis.municipios_summary" :key="mun.municipio" class="flex items-center justify-between p-3 bg-slate-50/80 hover:bg-blue-50/60 rounded-2xl transition border border-slate-100">
              <div>
                <div class="font-extrabold text-slate-900 text-xs">{{ mun.municipio }}</div>
                <div class="text-[10px] text-slate-500 font-medium mt-0.5">
                  <span class="text-emerald-700 font-bold">{{ mun.qr_asignados }} con QR</span> | {{ mun.sin_qr }} sin QR
                </div>
              </div>
              <div class="text-right">
                <span class="font-black text-slate-900 text-sm font-mono block">{{ mun.total_planteles }}</span>
                <span class="text-[10px] text-slate-400 font-bold uppercase">planteles</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  kpis: {
    type: Object,
    default: null
  }
})

function formatRolName(rol) {
  if (rol === 'DIRECTOR') return 'Directores de Plantel'
  if (rol === 'ENLACE_SEGEN') return 'Enlaces SEGEN'
  if (rol === 'SUPERVISOR') return 'Supervisores Educativos'
  if (rol === 'REPRESENTANTE') return 'Representantes de Institución Educativa'
  return rol
}
</script>
