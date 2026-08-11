import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
import { toast } from 'vue3-toastify'
import Swal from 'sweetalert2'

export function useGridData(activeTable) {
  const router = useRouter()
  const authStore = useAuthStore()

  const rows = ref([])
  const totalRows = ref(0)
  const loading = ref(false)
  const selectedRowsList = ref([])

  // Stacks de Deshacer / Rehacer
  const undoStack = ref([])
  const redoStack = ref([])

  const getTable = () => (typeof activeTable === 'string' ? activeTable : activeTable.value)

  // Carga de datos de la tabla activa
  async function loadTableData() {
    loading.value = true
    rows.value = []
    totalRows.value = 0
    selectedRowsList.value = []
    undoStack.value = []
    redoStack.value = []

    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (!token) {
        router.push('/admin/login')
        return
      }
      const resp = await axios.get(`/api/admin/data/${getTable()}`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { skip: 0, limit: 1000 }
      })
      rows.value = resp.data.items || []
      totalRows.value = resp.data.total || 0
    } catch (err) {
      console.error(err)
      if (err.response?.status === 401) {
        authStore.logoutAdmin()
        router.push('/admin/login')
      }
    } finally {
      loading.value = false
    }
  }

  // Cambio de valor de celda individual (PATCH)
  async function handleCellValueChanged({ row, column, newValue, oldValue }) {
    if (newValue === oldValue) return
    const rowId = row.id
    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (token) {
        await axios.patch(`/api/admin/data/${getTable()}/${rowId}`, {
          column, value: newValue
        }, { headers: { Authorization: `Bearer ${token}` } })
        undoStack.value.push({ rowId, column, oldValue, newValue })
        redoStack.value = []
        toast.success('Celda actualizada correctamente.')
      }
    } catch (err) {
      toast.error('Error al actualizar la celda en PostgreSQL.')
      console.error(err)
    }
  }

  // Guardar nuevo registro
  async function saveNewRow(newRowForm, onSuccess) {
    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (token) {
        await axios.post(`/api/admin/data/${getTable()}`, newRowForm, {
          headers: { Authorization: `Bearer ${token}` }
        })
        toast.success('Nuevo registro creado exitosamente.')
        if (onSuccess) onSuccess()
        await loadTableData()
      }
    } catch (err) {
      toast.error('Error al crear el nuevo registro.')
      console.error(err)
    }
  }

  // Eliminar registros (unitario o bulk)
  async function deleteRows(ids) {
    if (!ids || ids.length === 0) return
    const count = ids.length
    const result = await Swal.fire({
      title: 'Confirmar Eliminación',
      text: count === 1
        ? `Eliminar el registro #${ids[0]} de forma permanente?`
        : `Eliminar los ${count} registros seleccionados?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc2626',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Sí, Eliminar',
      cancelButtonText: 'Cancelar',
      customClass: { popup: 'rounded-3xl shadow-2xl font-sans' }
    })
    if (!result.isConfirmed) return
    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (token) {
        if (count === 1) {
          await axios.delete(`/api/admin/data/${getTable()}/${ids[0]}`, {
            headers: { Authorization: `Bearer ${token}` }
          })
        } else {
          await axios.post(`/api/admin/data/${getTable()}/bulk-delete`, { ids }, {
            headers: { Authorization: `Bearer ${token}` }
          })
        }
        selectedRowsList.value = []
        toast.success(`${count} registro(s) eliminado(s) exitosamente.`)
        await loadTableData()
      }
    } catch (err) {
      toast.error('Error al eliminar los registros.')
      console.error(err)
    }
  }

  function deleteSelectedRows() {
    const ids = selectedRowsList.value.map(r => r.id)
    deleteRows(ids)
  }

  // Deshacer cambio
  async function undo() {
    if (undoStack.value.length === 0) return
    const action = undoStack.value.pop()
    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (token) {
        await axios.patch(`/api/admin/data/${getTable()}/${action.rowId}`, {
          column: action.column, value: action.oldValue
        }, { headers: { Authorization: `Bearer ${token}` } })
        const targetRow = rows.value.find(r => r.id === action.rowId)
        if (targetRow) targetRow[action.column] = action.oldValue
        redoStack.value.push(action)
        toast.info(`Cambio deshecho en celda [${action.column}]`)
      }
    } catch (err) {
      toast.error('Error al deshacer el cambio.')
      undoStack.value.push(action)
    }
  }

  // Rehacer cambio
  async function redo() {
    if (redoStack.value.length === 0) return
    const action = redoStack.value.pop()
    try {
      const token = authStore.token || localStorage.getItem('admin_token')
      if (token) {
        await axios.patch(`/api/admin/data/${getTable()}/${action.rowId}`, {
          column: action.column, value: action.newValue
        }, { headers: { Authorization: `Bearer ${token}` } })
        const targetRow = rows.value.find(r => r.id === action.rowId)
        if (targetRow) targetRow[action.column] = action.newValue
        undoStack.value.push(action)
        toast.info(`Cambio rehecho en celda [${action.column}]`)
      }
    } catch (err) {
      toast.error('Error al rehacer el cambio.')
      redoStack.value.push(action)
    }
  }

  function handleSelectionChanged(selectedItems) {
    selectedRowsList.value = selectedItems
  }

  return {
    rows,
    totalRows,
    loading,
    selectedRowsList,
    undoStack,
    redoStack,
    loadTableData,
    handleCellValueChanged,
    saveNewRow,
    deleteRows,
    deleteSelectedRows,
    undo,
    redo,
    handleSelectionChanged
  }
}
