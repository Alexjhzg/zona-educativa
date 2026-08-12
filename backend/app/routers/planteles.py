from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

try:
    from ..database import get_db
    from ..models import Plantel
    from ..schemas import PlantelResponse
except ImportError:
    from database import get_db
    from models import Plantel
    from schemas import PlantelResponse

router = APIRouter(prefix="/api/planteles", tags=["Planteles Públicos"])

@router.get("/municipios", response_model=List[str])
def obtener_municipios_activos(db: Session = Depends(get_db)):
    """
    Retorna la lista única de municipios registrados en la base de datos, ordenados alfabéticamente.
    """
    results = db.query(Plantel.municipio_nombre).filter(
        Plantel.municipio_nombre.isnot(None),
        Plantel.municipio_nombre != ""
    ).distinct().order_by(Plantel.municipio_nombre.asc()).all()
    
    return [row[0].strip().upper() for row in results if row[0]]

def clean_ci_term(ci_str: str) -> str:
    """ Remueve V-, E-, puntos, guiones o decimales para comparar la cédula limpia """
    return ci_str.upper().replace("V-", "").replace("E-", "").replace(".", "").replace("-", "").replace(".0", "").strip()

@router.get("/search", response_model=List[PlantelResponse])
def buscar_planteles(
    q: str = Query(..., min_length=2, description="Buscar por Código DEA, Cédula del Director, Nombre o Municipio"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    Endpoint público de autocompletado para el Formulario de Solicitud de QR.
    Permite buscar por Código DEA, Cédula del Director, Nombre del Plantel o Municipio.
    """
    raw_term = q.strip()
    term = f"%{raw_term}%"
    ci_clean = clean_ci_term(raw_term)

    conditions = [
        Plantel.codigo_dea.ilike(term),
        Plantel.nombres_contacto.ilike(term),
        Plantel.plantel.ilike(term),
        Plantel.municipio_nombre.ilike(term)
    ]

    if ci_clean:
        conditions.append(Plantel.ci_contacto.ilike(f"%{ci_clean}%"))

    results = db.query(Plantel).filter(or_(*conditions)).limit(limit).all()
    return results

@router.get("/dea/{query_key}", response_model=PlantelResponse)
def obtener_plantel_por_dea_o_cedula(query_key: str, db: Session = Depends(get_db)):
    """
    Endpoint para buscar un plantel por su Código DEA o por la Cédula del Director.
    """
    clean_key = query_key.strip().upper()
    ci_clean = clean_ci_term(query_key)

    # 1. Búsqueda por DEA exacto
    plantel = db.query(Plantel).filter(Plantel.codigo_dea.ilike(clean_key)).first()
    
    # 2. Búsqueda por Cédula del Director
    if not plantel and ci_clean:
        plantel = db.query(Plantel).filter(
            (Plantel.ci_contacto.ilike(clean_key)) |
            (Plantel.ci_contacto == ci_clean)
        ).first()
    
    if not plantel:
        raise HTTPException(status_code=404, detail="Código DEA o Cédula no encontrada")
    return plantel

@router.get("/{plantel_id}", response_model=PlantelResponse)
def obtener_plantel_por_id(plantel_id: int, db: Session = Depends(get_db)):
    plantel = db.query(Plantel).filter(Plantel.id == plantel_id).first()
    if not plantel:
        raise HTTPException(status_code=404, detail="Plantel educativo no encontrado")
    return plantel
