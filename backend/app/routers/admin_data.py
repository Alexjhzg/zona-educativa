from typing import List, Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel

try:
    from ..database import get_db
    from ..models import Plantel, SolicitudQR, Municipio
    from .auth import get_current_admin
    from ..excel_importer import process_excel_import, generate_excel_template
    from ..services.backup_service import create_table_backup
except (ImportError, ModuleNotFoundError):
    try:
        from database import get_db
        from models import Plantel, SolicitudQR, Municipio
        from routers.auth import get_current_admin
        from excel_importer import process_excel_import, generate_excel_template
        from services.backup_service import create_table_backup
    except (ImportError, ModuleNotFoundError):
        from app.database import get_db
        from app.models import Plantel, SolicitudQR, Municipio
        from app.routers.auth import get_current_admin
        from app.excel_importer import process_excel_import, generate_excel_template
        from app.services.backup_service import create_table_backup

router = APIRouter(prefix="/api/admin/data", tags=["Administración de Tablas (Excel Grid)"])


class CellUpdatePayload(BaseModel):
    column: str
    value: Any

class BulkDeletePayload(BaseModel):
    ids: List[int]

import os

@router.get("/download-template/{table_name}")
def descargar_plantilla_excel(
    table_name: str = "planteles",
    admin_user = Depends(get_current_admin)
):
    """
    Retorna la plantilla oficial en formato .xlsx con el orden de columnas y tipos de datos estandarizados.
    """
    excel_bytes = generate_excel_template(table_name)
    headers = {
        'Content-Disposition': f'attachment; filename="PLANTILLA_OFICIAL_{table_name.upper()}.xlsx"'
    }
    return Response(
        content=excel_bytes,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )

@router.post("/{table_name}/upload-excel")
@router.post("/import-excel")
async def importar_excel_planteles(
    table_name: str = "planteles",
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """
    Recibe un archivo Excel (.xlsx / .xlsm / .csv) y realiza el Upsert atómico de la tabla,
    generando automáticamente un respaldo estructurado previo.
    """
    filename = file.filename.lower()
    if not (filename.endswith(".xlsx") or filename.endswith(".xlsm") or filename.endswith(".xls") or filename.endswith(".csv")):
        raise HTTPException(
            status_code=400,
            detail="Formato de archivo no válido. Solo se permiten archivos .xlsx, .xlsm, .xls o .csv."
        )

    # 1. Respaldo automático del estado actual
    try:
        backup_file_path = create_table_backup(db, table_name)
        backup_filename = os.path.basename(backup_file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error crítico: Falló la generación del respaldo automático para '{table_name}': {str(e)}"
        )

    # 2. Ingesta y Upsert masivo
    try:
        contents = await file.read()
        resumen = process_excel_import(contents, db)
        return {
            "message": f"Actualización masiva de la tabla '{table_name}' completada exitosamente.",
            "backup_file": backup_filename,
            "detalles": resumen
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo Excel: {str(e)}"
        )

@router.get("/{table_name}")
def listar_tabla(
    table_name: str,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=10000),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    if table_name == "planteles":
        query = db.query(Plantel)
        if q:
            search_str = f"%{q}%"
            query = query.filter(
                or_(
                    Plantel.codigo_dea.ilike(search_str),
                    Plantel.plantel.ilike(search_str),
                    Plantel.nombres_contacto.ilike(search_str),
                    Plantel.ci_contacto.ilike(search_str),
                    Plantel.municipio_nombre.ilike(search_str)
                )
            )
        total = query.count()
        items = query.order_by(Plantel.id.asc()).offset(skip).limit(limit).all()
        
        # Formatear a diccionarios limpios para la celda de Excel
        data = []
        for p in items:
            data.append({
                "id": p.id,
                "codigo_dea": p.codigo_dea or "",
                "plantel": p.plantel or "",
                "dependencia": p.dependencia or "",
                "denominacion": p.denominacion or "",
                "municipio_nombre": p.municipio_nombre or "",
                "parroquia_nombre": p.parroquia_nombre or "",
                "nombres_contacto": p.nombres_contacto or "",
                "ci_contacto": p.ci_contacto or "",
                "telefono_contacto": p.telefono_contacto or "",
                "email_contacto": p.email_contacto or "",
                "estatus_qr": p.estatus_qr or "SIN QR ASIGNADO",
                "estatus_segen": p.estatus_segen or "",
                "qr_segen": p.qr_segen or "",
                "qr_director": p.qr_director or "",
                "qr_director_sep": p.qr_director_sep or "",
                "qr_director_jul_2026": p.qr_director_jul_2026 or "",
                "rif": p.rif or "",
                "segmento": p.segmento or "",
                "manzana": p.manzana or "",
                "sector": p.sector or "",
                "centro_poblado": p.centro_poblado or "",
                "tipologia": p.tipologia or "",
                "ubicacion": p.ubicacion or "",
                "latitud": p.latitud,
                "longitud": p.longitud,
                "altitud": p.altitud,
                "precision_gps": p.precision_gps,
                "cedula_inmobiliaria_url": p.cedula_inmobiliaria_url or ""
            })
        return {"total": total, "skip": skip, "limit": limit, "items": data}

    elif table_name == "solicitudes_qr":
        query = db.query(SolicitudQR)
        if q:
            search_str = f"%{q}%"
            query = query.filter(
                or_(
                    SolicitudQR.solicitante_nombre.ilike(search_str),
                    SolicitudQR.solicitante_ci.ilike(search_str),
                    SolicitudQR.tipo_solicitud.ilike(search_str),
                    SolicitudQR.solicitante_rol.ilike(search_str)
                )
            )
        total = query.count()
        items = query.order_by(SolicitudQR.id.desc()).offset(skip).limit(limit).all()
        
        data = []
        for s in items:
            data.append({
                "id": s.id,
                "plantel_id": s.plantel_id,
                "tipo_solicitud": s.tipo_solicitud or "",
                "solicitante_rol": s.solicitante_rol or "",
                "solicitante_nombre": s.solicitante_nombre or "",
                "solicitante_ci": s.solicitante_ci or "",
                "solicitante_telefono": s.solicitante_telefono or "",
                "solicitante_email": s.solicitante_email or "",
                "estatus_solicitud": s.estatus_solicitud or "PENDIENTE",
                "motivo": s.motivo or ""
            })
        return {"total": total, "skip": skip, "limit": limit, "items": data}

    elif table_name == "municipios":
        query = db.query(Municipio)
        if q:
            query = query.filter(Municipio.nombre.ilike(f"%{q}%"))
        total = query.count()
        items = query.order_by(Municipio.id.asc()).offset(skip).limit(limit).all()
        
        data = [{"id": m.id, "nombre": m.nombre} for m in items]
        return {"total": total, "skip": skip, "limit": limit, "items": data}

    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")

@router.patch("/{table_name}/{row_id}")
def actualizar_celda(
    table_name: str,
    row_id: int,
    payload: CellUpdatePayload,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    model_class = None
    if table_name == "planteles":
        model_class = Plantel
    elif table_name == "solicitudes_qr":
        model_class = SolicitudQR
    elif table_name == "municipios":
        model_class = Municipio
    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")

    row = db.query(model_class).filter(model_class.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if not hasattr(row, payload.column):
        raise HTTPException(status_code=400, detail=f"Columna '{payload.column}' no existe en la tabla")

    # Actualizar la propiedad en la entidad SQLAlchemy
    setattr(row, payload.column, payload.value)
    
    # Efecto secundario: si se aprueba/procesa una solicitud en solicitudes_qr, actualizar el plantel
    if table_name == "solicitudes_qr" and payload.column == "estatus_solicitud" and payload.value in ["PROCESADO", "COMPLETADO"]:
        plantel = db.query(Plantel).filter(Plantel.id == row.plantel_id).first()
        if plantel:
            plantel.estatus_qr = "QR SEGEN"

    db.commit()
    db.refresh(row)

    return {"message": "Celda actualizada correctamente", "id": row_id, "column": payload.column, "value": payload.value}

@router.post("/{table_name}")
def crear_registro(
    table_name: str,
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    if table_name == "planteles":
        new_item = Plantel(**payload)
    elif table_name == "solicitudes_qr":
        new_item = SolicitudQR(**payload)
    elif table_name == "municipios":
        new_item = Municipio(**payload)
    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Registro creado exitosamente", "id": new_item.id}

@router.delete("/{table_name}/{row_id}")
def eliminar_registro(
    table_name: str,
    row_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    model_class = None
    if table_name == "planteles":
        model_class = Plantel
    elif table_name == "solicitudes_qr":
        model_class = SolicitudQR
    elif table_name == "municipios":
        model_class = Municipio
    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")

    row = db.query(model_class).filter(model_class.id == row_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(row)
    db.commit()
    return {"message": "Registro eliminado exitosamente", "id": row_id}

@router.post("/{table_name}/bulk-delete")
def eliminar_registros_lote(
    table_name: str,
    payload: BulkDeletePayload,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    model_class = None
    if table_name == "planteles":
        model_class = Plantel
    elif table_name == "solicitudes_qr":
        model_class = SolicitudQR
    elif table_name == "municipios":
        model_class = Municipio
    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")

    db.query(model_class).filter(model_class.id.in_(payload.ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": f"{len(payload.ids)} registros eliminados exitosamente", "ids": payload.ids}

