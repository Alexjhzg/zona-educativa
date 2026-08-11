from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

try:
    from ..database import get_db
    from ..models import SolicitudQR, Plantel
    from ..schemas import SolicitudCreate, SolicitudResponse
except ImportError:
    from database import get_db
    from models import SolicitudQR, Plantel
    from schemas import SolicitudCreate, SolicitudResponse

router = APIRouter(prefix="/api/solicitudes", tags=["Solicitudes QR"])

class EstatusUpdateSchema(BaseModel):
    estatus: Optional[str] = None
    nuevo_estatus: Optional[str] = None

@router.get("", response_model=List[SolicitudResponse])
def listar_solicitudes(db: Session = Depends(get_db)):
    """
    Obtener listado de todas las solicitudes registradas.
    """
    return db.query(SolicitudQR).options(joinedload(SolicitudQR.plantel)).order_by(SolicitudQR.fecha_solicitud.desc()).all()

@router.post("", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
def crear_solicitud_qr(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    """
    Endpoint público para que los solicitantes envíen una solicitud o reporte de código QR.
    """
    plantel = db.query(Plantel).filter(Plantel.id == solicitud.plantel_id).first()
    if not plantel:
        raise HTTPException(status_code=404, detail="El plantel especificado no existe")

    nueva_solicitud = SolicitudQR(
        plantel_id=solicitud.plantel_id,
        tipo_solicitud=solicitud.tipo_solicitud.upper(),
        solicitante_rol=solicitud.solicitante_rol.upper(),
        solicitante_nombre=solicitud.solicitante_nombre.strip(),
        solicitante_ci=solicitud.solicitante_ci.strip(),
        solicitante_telefono=solicitud.solicitante_telefono.strip(),
        solicitante_email=solicitud.solicitante_email.strip(),
        motivo=solicitud.motivo.strip() if solicitud.motivo else None,
        estatus_solicitud="PENDIENTE"
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    
    return nueva_solicitud

@router.patch("/{solicitud_id}/estatus")
def actualizar_estatus(solicitud_id: int, payload: EstatusUpdateSchema, db: Session = Depends(get_db)):
    sol = db.query(SolicitudQR).filter(SolicitudQR.id == solicitud_id).first()
    if not sol:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    estatus_final = payload.estatus or payload.nuevo_estatus or "PROCESADO"
    sol.estatus_solicitud = estatus_final.upper()
    
    if sol.estatus_solicitud in ["PROCESADO", "COMPLETADO"]:
        plantel = db.query(Plantel).filter(Plantel.id == sol.plantel_id).first()
        if plantel:
            plantel.estatus_qr = "QR SEGEN"
            
    db.commit()
    db.refresh(sol)
    return {"message": "Estatus actualizado correctamente", "id": sol.id, "estatus": sol.estatus_solicitud}
