<template>
  <div 
    ref="gridContainerRef"
    :class="isDark 
      ? 'ag-theme-quartz-dark border-white/10 shadow-xl' 
      : 'ag-theme-quartz border-slate-200 shadow-md'"
    class="relative w-full h-[650px] rounded-2xl overflow-hidden border select-none transition-colors duration-300"
    @click.stop="closeContextMenu"
    @contextmenu.prevent="onContainerContextMenu"
  >
    <AgGridVue
      class="w-full h-full text-xs font-sans"
      :theme="'legacy'"
      :modules="modules"
      :rowData="rowData"
      :columnDefs="computedColumnDefs"
      :defaultColDef="defaultColDef"
      :localeText="localeTextEs"
      :pagination="true"
      :paginationPageSize="100"
      :paginationPageSizeSelector="[50, 100, 250, 500, 1000]"
      :quickFilterText="quickFilterText"
      :singleClickEdit="true"
      :stopEditingWhenCellsLoseFocus="true"
      :navigateToNextCell="navigateToNextCell"
      :suppressConsoleDotLogs="true"
      :suppressPropertyNamesCheck="true"
      @grid-ready="onGridReady"
      @cell-value-changed="onCellValueChanged"
      @cell-clicked="onCellClicked"
      @cell-context-menu="onCellContextMenu"
      @selection-changed="onSelectionChanged"
      :rowSelection="rowSelectionConfig"
      :animateRows="true"
    />

    <!-- Menú Contextual de Clic Derecho Estilizado (Sapphire Glass) -->
    <GridContextMenu
      :visible="contextMenu.visible"
      :x="contextMenu.x"
      :y="contextMenu.y"
      :selected-count="selectedRowsCount"
      @action="handleContextMenuAction"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { AgGridVue } from 'ag-grid-vue3'
import { ModuleRegistry, AllCommunityModule } from 'ag-grid-community'
import { useTheme } from '../../composables/useTheme'
import GridContextMenu from './GridContextMenu.vue'

const emit = defineEmits(['grid-ready', 'cell-value-changed', 'selection-changed', 'delete-rows', 'show-qr-modal'])

const { isDark } = useTheme()

import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'

// Registrar todos los módulos comunitarios de AG-Grid para AG-Grid v36
ModuleRegistry.registerModules([AllCommunityModule])
const modules = [AllCommunityModule]

const rowSelectionConfig = computed(() => ({
  mode: 'multiRow',
  enableClickSelection: true
}))

// Diccionario de Localización Oficial en Español para AG-Grid
const localeTextEs = {
  filterOoo: 'Filtrar...',
  equals: 'Es igual a',
  notEqual: 'No es igual a',
  blank: 'Está en blanco',
  notBlank: 'No está en blanco',
  empty: 'Seleccione una opción',
  contains: 'Contiene',
  notContains: 'No contiene',
  startsWith: 'Empieza con',
  endsWith: 'Termina con',
  lessThan: 'Menor que',
  greaterThan: 'Mayor que',
  lessThanOrEqual: 'Menor o igual que',
  greaterThanOrEqual: 'Mayor o igual que',
  inRange: 'En el rango',
  selectAll: '(Seleccionar todo)',
  searchOoo: 'Buscar en filtro...',
  blanks: '(En blanco)',
  noMatches: 'No se encontraron coincidencias',
  applyFilter: 'Aplicar',
  resetFilter: 'Restablecer',
  clearFilter: 'Limpiar',
  cancelFilter: 'Cancelar',
  page: 'Página',
  to: 'a',
  of: 'de',
  nextPage: 'Siguiente Página',
  lastPage: 'Última Página',
  firstPage: 'Primera Página',
  previousPage: 'Página Anterior',
  loadingOoo: 'Cargando registros...',
  noRowsToShow: 'No hay datos para mostrar',
  andCondition: 'Y',
  orCondition: 'O'
}

const props = defineProps({
  rowData: {
    type: Array,
    default: () => []
  },
  columnDefs: {
    type: Array,
    default: () => []
  },
  quickFilterText: {
    type: String,
    default: ''
  }
})

const gridApi = ref(null)
const gridContainerRef = ref(null)
const selectedRows = ref([])

const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  cellValue: '',
  rowData: null
})

watch(() => props.rowData, (newRows) => {
  if (gridApi.value && newRows) {
    gridApi.value.setGridOption('rowData', newRows)
  }
}, { deep: true })

const selectedRowsCount = computed(() => {
  return selectedRows.value.length > 0 ? selectedRows.value.length : (contextMenu.value.rowData ? 1 : 0)
})

const defaultColDef = {
  sortable: true,
  filter: true,
  resizable: true,
  editable: true,
  flex: 1,
  minWidth: 130
}

const computedColumnDefs = computed(() => {
  return props.columnDefs
})

onMounted(() => {
  window.addEventListener('scroll', closeContextMenu)
  document.addEventListener('click', handleGlobalClick)
})

onUnmounted(() => {
  window.removeEventListener('scroll', closeContextMenu)
  document.removeEventListener('click', handleGlobalClick)
})

function navigateToNextCell(params) {
  const suggestedNextCell = params.nextCellPosition
  if (!suggestedNextCell) return null

  if (params.key === 'ArrowUp' || params.key === 'ArrowDown') {
    if (params.api) {
      const rowNode = params.api.getDisplayedRowAtIndex(suggestedNextCell.rowIndex)
      if (rowNode) {
        rowNode.setSelected(true, true)
      }
    }
  }

  return suggestedNextCell
}

function handleGlobalClick(e) {
  closeContextMenu()
  if (gridContainerRef.value && !gridContainerRef.value.contains(e.target)) {
    if (gridApi.value) {
      gridApi.value.deselectAll()
    }
  }
}

function onGridReady(params) {
  gridApi.value = params.api
  emit('grid-ready', params.api)
}

function onCellValueChanged(event) {
  emit('cell-value-changed', {
    row: event.data,
    column: event.colDef.field,
    newValue: event.newValue,
    oldValue: event.oldValue
  })
}

function onCellClicked(event) {
  // Si se hizo clic en un botón con atributo data-action="ver-qr"
  if (event.event && event.event.target) {
    const actionBtn = event.event.target.closest('[data-action="ver-qr"]')
    if (actionBtn && event.data) {
      emit('show-qr-modal', event.data)
      return
    }
  }
  
  if (event.colDef && event.colDef.field === 'ver_qr_action' && event.data) {
    emit('show-qr-modal', event.data)
  }
}

function onSelectionChanged() {
  if (gridApi.value) {
    selectedRows.value = gridApi.value.getSelectedRows()
    emit('selection-changed', selectedRows.value)
  }
}

function onContainerContextMenu(e) {
  e.preventDefault()
  e.stopPropagation()
}

function onCellContextMenu(params) {
  if (params.event) {
    params.event.preventDefault()
    params.event.stopPropagation()
  }
  
  const node = params.node
  if (node && !node.isSelected()) {
    node.setSelected(true)
  }

  const mouseX = params.event ? params.event.clientX : 100
  const mouseY = params.event ? params.event.clientY : 100

  contextMenu.value = {
    visible: true,
    x: Math.min(mouseX, window.innerWidth - 220),
    y: Math.min(mouseY, window.innerHeight - 150),
    cellValue: params.value,
    rowData: params.data
  }
}

function closeContextMenu() {
  contextMenu.value.visible = false
}

function handleContextMenuAction(action) {
  if (action === 'ver-qr') {
    triggerShowQrModal()
  } else if (action === 'copiar') {
    copySelectedCellValue()
  } else if (action === 'eliminar') {
    triggerDeleteSelected()
  }
}

function triggerShowQrModal() {
  const rowToOpen = selectedRows.value.length > 0 ? selectedRows.value[0] : contextMenu.value.rowData
  if (rowToOpen) {
    emit('show-qr-modal', rowToOpen)
  }
  closeContextMenu()
}

function copySelectedCellValue() {
  if (contextMenu.value.cellValue !== undefined && contextMenu.value.cellValue !== null) {
    navigator.clipboard.writeText(String(contextMenu.value.cellValue))
  }
  closeContextMenu()
}

function triggerDeleteSelected() {
  const idsToDelete = selectedRows.value.length > 0 
    ? selectedRows.value.map(r => r.id) 
    : (contextMenu.value.rowData ? [contextMenu.value.rowData.id] : [])
  
  if (idsToDelete.length > 0) {
    emit('delete-rows', idsToDelete)
  }
  closeContextMenu()
}

defineExpose({
  exportCsv() {
    if (gridApi.value) {
      gridApi.value.exportDataAsCsv({
        suppressQuotes: false
      })
    }
  }
})
</script>

<style>
/* Tema Claro Nordic Clean para AG-Grid */
.ag-theme-quartz {
  --ag-font-family: 'Inter', 'Geist', system-ui, sans-serif;
  --ag-font-size: 12px;
  --ag-background-color: #ffffff;
  --ag-odd-row-background-color: #f8fafc;
  --ag-header-background-color: #f1f5f9;
  --ag-header-foreground-color: #334155;
  --ag-border-color: #e2e8f0;
  --ag-row-border-color: #f1f5f9;
  --ag-row-hover-color: #f0f9ff;
  --ag-selected-row-background-color: #e0f2fe;
  --ag-foreground-color: #0f172a;
  --ag-secondary-foreground-color: #64748b;
  --ag-cell-horizontal-padding: 12px;
}
.ag-theme-quartz .ag-header-cell-label {
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 11px;
  color: #475569;
}
.ag-theme-quartz .ag-paging-panel {
  color: #475569;
  font-size: 12px;
  border-top: 1px solid #e2e8f0;
}

/* Tema Oscuro Sapphire Glass para AG-Grid - /admin/excel-grid */
.ag-theme-quartz-dark {
  --ag-font-family: 'Inter', 'Geist', system-ui, sans-serif;
  --ag-font-size: 12px;
  /* Fondo base sapphire */
  --ag-background-color: #0d1c2d;
  --ag-odd-row-background-color: #051424;
  /* Header oscuro */
  --ag-header-background-color: #010f1f;
  --ag-header-foreground-color: #d4e4fa;
  /* Bordes sapphire */
  --ag-border-color: rgba(255,255,255,0.08);
  --ag-row-border-color: rgba(255,255,255,0.05);
  /* Hover y selección con acento verde */
  --ag-row-hover-color: rgba(78, 222, 163, 0.05);
  --ag-selected-row-background-color: rgba(123, 208, 255, 0.1);
  /* Texto */
  --ag-foreground-color: #d4e4fa;
  --ag-secondary-foreground-color: #94a3b8;
  /* Input de filtros */
  --ag-input-border-color: rgba(255,255,255,0.15);
  --ag-input-focus-border-color: #4edea3;
  --ag-input-background-color: #0d1c2d;
  --ag-input-foreground-color: #d4e4fa;
  /* Paginación */
  --ag-pagination-background-color: #010f1f;
  --ag-control-panel-background-color: #0d1c2d;
  /* Menú */
  --ag-menu-background-color: #122131;
  --ag-menu-border-color: rgba(255,255,255,0.1);
  /* Cell padding */
  --ag-cell-horizontal-padding: 12px;
  /* Wrapper */
  --ag-wrapper-border-radius: 0;
  --ag-border-radius: 0;
}
.ag-theme-quartz-dark .ag-header-cell-label {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 11px;
  color: #94a3b8;
}
.ag-theme-quartz-dark .ag-header-cell {
  border-right: 1px solid rgba(255,255,255,0.06);
}
.ag-theme-quartz-dark .ag-paging-panel {
  color: #94a3b8;
  font-size: 12px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.ag-theme-quartz-dark .ag-cell-focus {
  border: 1px solid rgba(78, 222, 163, 0.5) !important;
}
.ag-theme-quartz-dark .ag-row-selected {
  background-color: rgba(123, 208, 255, 0.08) !important;
}
.ag-theme-quartz-dark .ag-ltr .ag-cell {
  border-right: 1px solid rgba(255,255,255,0.04);
}
</style>
