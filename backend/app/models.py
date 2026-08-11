from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

try:
    from .database import Base
except ImportError:
    from database import Base

class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)

    parroquias = relationship("Parroquia", back_populates="municipio")
    planteles = relationship("Plantel", back_populates="municipio_rel")

class Parroquia(Base):
    __tablename__ = "parroquias"

    id = Column(Integer, primary_key=True, index=True)
    municipio_id = Column(Integer, ForeignKey("municipios.id"), nullable=False)
    nombre = Column(String(100), nullable=False, index=True)

    municipio = relationship("Municipio", back_populates="parroquias")
    planteles = relationship("Plantel", back_populates="parroquia_rel")

class Plantel(Base):
    __tablename__ = "planteles"

    id = Column(Integer, primary_key=True, index=True)
    codigo_dea = Column(String(50), unique=True, index=True, nullable=False)
    plantel = Column(String(255), nullable=False, index=True)
    eponimo_anterior = Column(String(255), nullable=True)
    dependencia = Column(String(100), nullable=False, index=True)
    denominacion = Column(String(100), nullable=True)
    direccion = Column(Text, nullable=True)
    comunidad = Column(String(150), nullable=True)
    
    # Contacto actual según Excel
    nombres_contacto = Column(String(200), nullable=True)
    ci_contacto = Column(String(50), nullable=True)
    telefono_contacto = Column(String(50), nullable=True)
    email_contacto = Column(String(150), nullable=True)

    # Estatus de Levantamiento
    estatus_zona = Column(String(100), nullable=True)
    estatus_segen = Column(String(100), nullable=True, index=True)
    estatus_director = Column(String(100), nullable=True, index=True)
    estatus_qr = Column(String(100), nullable=False, index=True)

    # Códigos QR asignados
    qr_segen = Column(String(100), nullable=True)
    qr_director = Column(String(100), nullable=True)
    qr_director_sep = Column(String(100), nullable=True)
    qr_director_jul_2026 = Column(String(100), nullable=True)

    # Ubicación
    municipio_id = Column(Integer, ForeignKey("municipios.id"), nullable=True)
    parroquia_id = Column(Integer, ForeignKey("parroquias.id"), nullable=True)
    municipio_nombre = Column(String(100), nullable=True, index=True)
    parroquia_nombre = Column(String(100), nullable=True)
    
    # Datos Geográficos y Territoriales Adicionales
    rif = Column(String(50), nullable=True)
    segmento = Column(String(100), nullable=True)
    manzana = Column(String(100), nullable=True)
    sector = Column(String(150), nullable=True)
    centro_poblado = Column(String(150), nullable=True)
    tipologia = Column(String(100), nullable=True)
    ubicacion = Column(String(255), nullable=True)
    
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    altitud = Column(Float, nullable=True)
    precision_gps = Column(Float, nullable=True)
    cedula_inmobiliaria_url = Column(String(255), nullable=True)

    municipio_rel = relationship("Municipio", back_populates="planteles")
    parroquia_rel = relationship("Parroquia", back_populates="planteles")
    solicitudes = relationship("SolicitudQR", back_populates="plantel")

class SolicitudQR(Base):
    __tablename__ = "solicitudes_qr"

    id = Column(Integer, primary_key=True, index=True)
    plantel_id = Column(Integer, ForeignKey("planteles.id"), nullable=False)
    
    # Tipo de requerimiento: NUEVA_ASIGNACION, REPOSICION, CORRECCION
    tipo_solicitud = Column(String(50), nullable=False, index=True)
    
    # Rol del Solicitante: DIRECTOR, ENLACE_SEGEN, SUPERVISOR, REPRESENTANTE
    solicitante_rol = Column(String(50), nullable=False, index=True)
    solicitante_nombre = Column(String(200), nullable=False)
    solicitante_ci = Column(String(50), nullable=False)
    solicitante_telefono = Column(String(50), nullable=False)
    solicitante_email = Column(String(150), nullable=False)
    
    motivo = Column(Text, nullable=True)
    
    # Estatus de atención: PENDIENTE, EN_PROCESO, APROBADA, RECHAZADA
    estatus_solicitud = Column(String(50), default="PENDIENTE", index=True)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow, index=True)

    plantel = relationship("Plantel", back_populates="solicitudes")

class UsuarioAdmin(Base):
    __tablename__ = "usuarios_admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    activo = Column(Integer, default=1)
