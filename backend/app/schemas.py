from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlantelBase(BaseModel):
    codigo_dea: str
    plantel: str
    dependencia: str
    denominacion: str | None = None
    direccion: str | None = None
    comunidad: str | None = None
    municipio_nombre: str | None = None
    parroquia_nombre: str | None = None
    nombres_contacto: str | None = None
    ci_contacto: str | None = None
    telefono_contacto: str | None = None
    email_contacto: str | None = None
    estatus_qr: str
    estatus_segen: str | None = None
    estatus_director: str | None = None
    rif: str | None = None
    segmento: str | None = None
    manzana: str | None = None
    sector: str | None = None
    centro_poblado: str | None = None
    tipologia: str | None = None
    ubicacion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    altitud: float | None = None
    precision_gps: float | None = None
    cedula_inmobiliaria_url: str | None = None


class PlantelResponse(PlantelBase):
    id: int
    qr_segen: str | None = None
    qr_director: str | None = None
    qr_director_sep: str | None = None
    qr_director_jul_2026: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SolicitudCreate(BaseModel):
    plantel_id: int
    tipo_solicitud: str  # NUEVA_ASIGNACION, REPOSICION, CORRECCION
    solicitante_rol: str  # DIRECTOR, ENLACE_SEGEN, SUPERVISOR, REPRESENTANTE
    solicitante_nombre: str
    solicitante_ci: str
    solicitante_telefono: str
    solicitante_email: str
    motivo: str | None = None


class SolicitudResponse(SolicitudCreate):
    id: int
    estatus_solicitud: str
    fecha_solicitud: datetime
    plantel: PlantelResponse | None = None

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
    top_solicitante_rol: str | None
    ranking_roles: list[RolKpi]
    estatus_qr_breakdown: list[EstatusQrKpi]
    municipios_summary: list[MunicipioKpi]
