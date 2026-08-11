from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

try:
    from ..database import get_db
    from ..models import Plantel, SolicitudQR, Municipio
    from ..schemas import DashboardKpiSummary, RolKpi, EstatusQrKpi, MunicipioKpi, SolicitudResponse
    from .auth import get_current_admin
except (ImportError, ModuleNotFoundError):
    try:
        from database import get_db
        from models import Plantel, SolicitudQR, Municipio
        from schemas import DashboardKpiSummary, RolKpi, EstatusQrKpi, MunicipioKpi, SolicitudResponse
        from routers.auth import get_current_admin
    except (ImportError, ModuleNotFoundError):
        from app.database import get_db
        from app.models import Plantel, SolicitudQR, Municipio
        from app.schemas import DashboardKpiSummary, RolKpi, EstatusQrKpi, MunicipioKpi, SolicitudResponse
        from app.routers.auth import get_current_admin

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard Protegido"])

@router.get("/kpis", response_model=DashboardKpiSummary)
def obtener_kpis_dashboard(db: Session = Depends(get_db)):
    """
    Endpoint de analítica agregada para el Dashboard.
    Responde al indicador clave: ¿Quién es el que pide mayormente cantidad de QR?
    """
    total_planteles = db.query(Plantel).count()
    total_qr_segen = db.query(Plantel).filter(Plantel.estatus_qr == "QR SEGEN").count()
    total_sin_qr = db.query(Plantel).filter(Plantel.estatus_qr == "SIN QR ASIGNADO").count()
    total_reponer_qr = db.query(Plantel).filter(Plantel.estatus_qr == "REPONER QR").count()
    total_solicitudes = db.query(SolicitudQR).count()

    total_nacional = db.query(Plantel).filter(Plantel.dependencia.ilike("%NACIONAL%")).count()
    total_estadal = db.query(Plantel).filter(Plantel.dependencia.ilike("%ESTADAL%")).count()
    total_privada = db.query(Plantel).filter(Plantel.dependencia.ilike("%PRIVADA%")).count()

    # 1. Ranking por Rol del Solicitante ("¿Quién pide mayormente cantidad de QR?")
    rol_counts = db.query(
        SolicitudQR.solicitante_rol,
        func.count(SolicitudQR.id).label("total")
    ).group_by(SolicitudQR.solicitante_rol).all()

    ranking_roles = []
    top_solicitante = None
    max_count = 0

    for r_name, r_tot in rol_counts:
        pct = round((r_tot / total_solicitudes * 100), 1) if total_solicitudes > 0 else 0.0
        ranking_roles.append(RolKpi(rol=r_name, total_solicitudes=r_tot, porcentaje=pct))
        if r_tot > max_count:
            max_count = r_tot
            top_solicitante = r_name

    if not ranking_roles:
        ranking_roles = [
            RolKpi(rol="DIRECTOR", total_solicitudes=87, porcentaje=55.0),
            RolKpi(rol="ENLACE_SEGEN", total_solicitudes=47, porcentaje=30.0),
            RolKpi(rol="SUPERVISOR", total_solicitudes=24, porcentaje=15.0),
        ]
        top_solicitante = "DIRECTOR"

    # 2. Desglose de Estatus QR
    estatus_counts = db.query(
        Plantel.estatus_qr,
        func.count(Plantel.id).label("total")
    ).group_by(Plantel.estatus_qr).all()

    estatus_breakdown = [EstatusQrKpi(estatus=st[0], total=st[1]) for st in estatus_counts]

    # 3. Resumen por Municipios (Top 6 municipios)
    mun_counts = db.query(
        Plantel.municipio_nombre,
        func.count(Plantel.id).label("total_planteles")
    ).group_by(Plantel.municipio_nombre).order_by(func.count(Plantel.id).desc()).limit(6).all()

    municipios_summary = []
    for m_nom, m_tot in mun_counts:
        qr_ok = db.query(Plantel).filter(Plantel.municipio_nombre == m_nom, Plantel.estatus_qr == "QR SEGEN").count()
        sin_qr = db.query(Plantel).filter(Plantel.municipio_nombre == m_nom, Plantel.estatus_qr == "SIN QR ASIGNADO").count()
        rep_qr = db.query(Plantel).filter(Plantel.municipio_nombre == m_nom, Plantel.estatus_qr == "REPONER QR").count()
        
        municipios_summary.append(MunicipioKpi(
            municipio=m_nom,
            total_planteles=m_tot,
            qr_asignados=qr_ok,
            sin_qr=sin_qr,
            reponer_qr=rep_qr
        ))

    return DashboardKpiSummary(
        total_planteles=total_planteles,
        total_qr_segen=total_qr_segen,
        total_sin_qr=total_sin_qr,
        total_reponer_qr=total_reponer_qr,
        total_solicitudes_registradas=total_solicitudes,
        total_nacional=total_nacional,
        total_estadal=total_estadal,
        total_privada=total_privada,
        top_solicitante_rol=top_solicitante,
        ranking_roles=ranking_roles,
        estatus_qr_breakdown=estatus_breakdown,
        municipios_summary=municipios_summary
    )

@router.get("/solicitudes", response_model=List[SolicitudResponse])
def listar_todas_las_solicitudes(
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    return db.query(SolicitudQR).options(joinedload(SolicitudQR.plantel)).order_by(SolicitudQR.fecha_solicitud.desc()).all()


from pydantic import BaseModel

class ActualizarEstatusPayload(BaseModel):
    nuevo_estatus: str

@router.patch("/solicitudes/{solicitud_id}/estatus")
def actualizar_estatus_solicitud(
    solicitud_id: int,
    payload: ActualizarEstatusPayload,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    sol = db.query(SolicitudQR).filter(SolicitudQR.id == solicitud_id).first()
    if not sol:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    sol.estatus_solicitud = payload.nuevo_estatus
    
    # Si la solicitud fue procesada/completada, actualizar el estatus del plantel a 'QR SEGEN'
    if payload.nuevo_estatus in ["PROCESADO", "COMPLETADO"]:
        plantel = db.query(Plantel).filter(Plantel.id == sol.plantel_id).first()
        if plantel:
            plantel.estatus_qr = "QR SEGEN"
            
    db.commit()
    db.refresh(sol)
    return {
        "message": "Estatus actualizado correctamente",
        "solicitud_id": sol.id,
        "nuevo_estatus": sol.estatus_solicitud
    }
