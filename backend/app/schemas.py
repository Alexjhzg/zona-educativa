from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class PlantelBase(BaseModel):
    codigo_dea: str
    plantel: str
    dependencia: str
    denominacion: Optional[str] = None
    direccion: Optional[str] = None
    comunidad: Optional[str] = None
    municipio_nombre: Optional[str] = None
    parroquia_nombre: Optional[str] = None
    nombres_contacto: Optional[str] = None
    ci_contacto: Optional[str] = None
    telefono_contacto: Optional[str] = None
    email_contacto: Optional[str] = None
    estatus_qr: str
    estatus_segen: Optional[str] = None
    estatus_director: Optional[str] = None
    rif: Optional[str] = None
    segmento: Optional[str] = None
    manzana: Optional[str] = None
    sector: Optional[str] = None
    centro_poblado: Optional[str] = None
    tipologia: Optional[str] = None
    ubicacion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    altitud: Optional[float] = None
    precision_gps: Optional[float] = None
    cedula_inmobiliaria_url: Optional[str] = None

class PlantelResponse(PlantelBase):
    id: int
    qr_segen: Optional[str] = None
    qr_director: Optional[str] = None
    qr_director_sep: Optional[str] = None
    qr_director_jul_2026: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SolicitudCreate(BaseModel):
    plantel_id: int
    tipo_solicitud: str  # NUEVA_ASIGNACION, REPOSICION, CORRECCION
    solicitante_rol: str  # DIRECTOR, ENLACE_SEGEN, SUPERVISOR, REPRESENTANTE
    solicitante_nombre: str
    solicitante_ci: str
    solicitante_telefono: str
    solicitante_email: str
    motivo: Optional[str] = None

class SolicitudResponse(SolicitudCreate):
    id: int
    estatus_solicitud: str
    fecha_solicitud: datetime
    plantel: Optional[PlantelResponse] = None

    model_config = ConfigDict(from_attributes=True)

# Dashboard KPI Schemas
class RolKpi(BaseModel):
    rol: str
    total_solicitudes: int
    porcentaje: float

class MunicipioKpi(BaseModel):
    municipio: str
    total_planteles: int
    qr_asignados: int
    sin_qr: int
    reponer_qr: int

class EstatusQrKpi(BaseModel):
    estatus: str
    total: int

class DashboardKpiSummary(BaseModel):
    total_planteles: int
    total_qr_segen: int
    total_sin_qr: int
    total_reponer_qr: int
    total_solicitudes_registradas: int
    total_nacional: int = 0
    total_estadal: int = 0
    total_privada: int = 0
    top_solicitante_rol: Optional[str]
    ranking_roles: List[RolKpi]
    estatus_qr_breakdown: List[EstatusQrKpi]
    municipios_summary: List[MunicipioKpi]
