import { computed } from 'vue'
import {
  MUNICIPIOS_MONAGAS,
  DEPENDENCIAS,
  ESTATUS_QR_LIST,
  ROLES_LIST,
  TIPO_SOLICITUD_LIST,
  ESTATUS_SOLICITUD_LIST
} from '../constants/gridOptions'

export function useColumnDefs(activeTable) {
  const columnDefs = computed(() => {
    const currentTable = typeof activeTable === 'string' ? activeTable : activeTable.value
    if (currentTable === 'planteles') {
      return [
        {
          headerName: 'QR',
          field: 'ver_qr_action',
          width: 110,
          flex: 0,
          editable: false,
          sortable: false,
          filter: false,
          cellRenderer: () => {
            return `<button
              title="Ver códigos QR"
              data-action="ver-qr"
              style="
                display:inline-flex;
                align-items:center;
                gap:5px;
                padding:2px 8px;
                border-radius:6px;
                background:rgba(78,222,163,0.15);
                color:#4edea3;
                font-size:11px;
                font-weight:700;
                border:1px solid rgba(78,222,163,0.3);
                cursor:pointer;
                line-height:1.4;
                transition:background 0.15s,color 0.15s;
              "
              onmouseover="this.style.background='#4edea3';this.style.color='#051424'"
              onmouseout="this.style.background='rgba(78,222,163,0.15)';this.style.color='#4edea3'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/></svg>
              Código QR
            </button>`
          }
        },
        { field: 'id', headerName: 'ID', width: 70, editable: false, flex: 0 },
        {
          field: 'municipio_nombre',
          headerName: 'Municipio',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: MUNICIPIOS_MONAGAS },
          filter: true
        },
        { field: 'parroquia_nombre', headerName: 'Parroquia', filter: true },
        { field: 'codigo_dea', headerName: 'Código DEA', filter: true },
        { field: 'plantel', headerName: 'Nombre del Plantel', filter: true, flex: 2 },
        {
          field: 'dependencia',
          headerName: 'Dependencia',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: DEPENDENCIAS },
          filter: true
        },
        { field: 'nombres_contacto', headerName: 'Contacto / Director', filter: true },
        { field: 'ci_contacto', headerName: 'Cédula Director', filter: true },
        { field: 'telefono_contacto', headerName: 'Teléfono Director', filter: true },
        { field: 'email_contacto', headerName: 'Correo Director', filter: true },
        {
          field: 'estatus_qr',
          headerName: 'Estatus QR',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: ESTATUS_QR_LIST },
          filter: true
        },
        { field: 'qr_segen', headerName: 'QR SEGEN', filter: true, width: 140 },
        { field: 'qr_director', headerName: 'QR Director Actual', filter: true, width: 170 },
        { field: 'qr_director_sep', headerName: 'QR Director SEP', filter: true, width: 170 },
        { field: 'qr_director_jul_2026', headerName: 'QR Director Jul 2026', filter: true, width: 180 },
        { field: 'rif', headerName: 'RIF', filter: true, width: 130 },
        { field: 'segmento', headerName: 'Segmento', filter: true, width: 130 },
        { field: 'manzana', headerName: 'Manzana', filter: true, width: 130 },
        { field: 'sector', headerName: 'Sector', filter: true, width: 160 },
        { field: 'centro_poblado', headerName: 'Centro Poblado', filter: true, width: 160 },
        { field: 'tipologia', headerName: 'Tipología', filter: true, width: 150 },
        { field: 'ubicacion', headerName: 'Ubicación', filter: true, width: 180 },
        { field: 'latitud', headerName: 'Latitud', filter: true, width: 130 },
        { field: 'longitud', headerName: 'Longitud', filter: true, width: 130 },
        { field: 'altitud', headerName: 'Altitud', filter: true, width: 120 },
        { field: 'precision_gps', headerName: 'Precisión', filter: true, width: 120 }
      ]
    } else if (currentTable === 'solicitudes_qr') {
      return [
        { field: 'id', headerName: 'ID', width: 70, editable: false, flex: 0 },
        { field: 'solicitante_nombre', headerName: 'Solicitante', filter: true },
        { field: 'solicitante_ci', headerName: 'Cédula', filter: true },
        {
          field: 'solicitante_rol',
          headerName: 'Rol Solicitante',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: ROLES_LIST },
          filter: true
        },
        {
          field: 'tipo_solicitud',
          headerName: 'Tipo Trámite',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: TIPO_SOLICITUD_LIST },
          filter: true
        },
        {
          field: 'estatus_solicitud',
          headerName: 'Estatus',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: ESTATUS_SOLICITUD_LIST },
          filter: true
        },
        { field: 'motivo', headerName: 'Observación / Motivo', filter: true }
      ]
    } else if (currentTable === 'municipios') {
      return [
        { field: 'id', headerName: 'ID', width: 70, editable: false, flex: 0 },
        {
          field: 'nombre',
          headerName: 'Nombre del Municipio',
          cellEditor: 'agSelectCellEditor',
          cellEditorParams: { values: MUNICIPIOS_MONAGAS },
          filter: true
        }
      ]
    }
    return []
  })

  const modalColumns = computed(() => {
    return columnDefs.value.map(col => ({
      key: col.field,
      label: col.headerName,
      type: col.cellEditor === 'agSelectCellEditor' ? 'select' : 'text',
      options: col.cellEditorParams ? col.cellEditorParams.values : []
    }))
  })

  return {
    columnDefs,
    modalColumns
  }
}
