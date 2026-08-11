import os
import bcrypt
import pandas as pd
from sqlalchemy import func
try:
    from .database import engine, SessionLocal, Base
    from .models import Municipio, Parroquia, Plantel, SolicitudQR, UsuarioAdmin
except (ImportError, ModuleNotFoundError):
    try:
        from database import engine, SessionLocal, Base
        from models import Municipio, Parroquia, Plantel, SolicitudQR, UsuarioAdmin
    except (ImportError, ModuleNotFoundError):
        from app.database import engine, SessionLocal, Base
        from app.models import Municipio, Parroquia, Plantel, SolicitudQR, UsuarioAdmin

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def clean_str(val):
    if pd.isna(val) or val is None:
        return None
    val_str = str(val).strip()
    return val_str if val_str else None

def standardize_dependencia(val):
    clean = clean_str(val)
    if not clean:
        return "NO ESPECIFICADA"
    upper = clean.upper()
    if "NACIONAL" in upper:
        return "NACIONAL"
    elif "ESTADAL" in upper:
        return "ESTADAL"
    elif "PRIVADA SUBVENCIONADA" in upper:
        return "PRIVADA SUBVENCIONADA"
    elif "PRIVADA" in upper:
        return "PRIVADA"
    elif "MUNICIPAL" in upper:
        return "MUNICIPAL"
    elif "AUTÓNOMA" in upper or "AUTONOMA" in upper:
        return "AUTÓNOMA"
    return upper

def seed_database(xlsm_path):
    print(f"🚀 Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Verificar si ya existen planteles cargados
    existing_count = db.query(Plantel).count()
    if existing_count > 0:
        print(f"ℹ️ La base de datos contiene {existing_count} planteles cargados.")
    else:
        print(f"📦 Leyendo archivo Excel: {xlsm_path}")
        df = pd.read_excel(xlsm_path, sheet_name='planteles')
        print(f"Total registros en Excel: {len(df)}")
        
        municipios_map = {}
        parroquias_map = {}
        
        planteles_to_insert = []
        
        for idx, row in df.iterrows():
            mun_nom = clean_str(row.get('MUNICIPIO')) or "MATURIN"
            parr_nom = clean_str(row.get('PARROQUIA')) or "SIN PARROQUIA"
            
            # Crear o buscar Municipio
            mun_nom_clean = mun_nom.upper().strip()
            if mun_nom_clean not in municipios_map:
                mun_obj = db.query(Municipio).filter(func.upper(Municipio.nombre) == mun_nom_clean).first()
                if not mun_obj:
                    try:
                        mun_obj = Municipio(nombre=mun_nom_clean)
                        db.add(mun_obj)
                        db.commit()
                        db.refresh(mun_obj)
                    except Exception:
                        db.rollback()
                        mun_obj = db.query(Municipio).filter(func.upper(Municipio.nombre) == mun_nom_clean).first()
                municipios_map[mun_nom_clean] = mun_obj.id
            mun_id = municipios_map[mun_nom_clean]
            
            # Crear o buscar Parroquia
            parr_nom_clean = parr_nom.upper().strip()
            parr_key = f"{mun_id}_{parr_nom_clean}"
            if parr_key not in parroquias_map:
                parr_obj = db.query(Parroquia).filter(
                    Parroquia.municipio_id == mun_id,
                    func.upper(Parroquia.nombre) == parr_nom_clean
                ).first()
                if not parr_obj:
                    try:
                        parr_obj = Parroquia(municipio_id=mun_id, nombre=parr_nom_clean)
                        db.add(parr_obj)
                        db.commit()
                        db.refresh(parr_obj)
                    except Exception:
                        db.rollback()
                        parr_obj = db.query(Parroquia).filter(
                            Parroquia.municipio_id == mun_id,
                            func.upper(Parroquia.nombre) == parr_nom_clean
                        ).first()
                parroquias_map[parr_key] = parr_obj.id
            parr_id = parroquias_map[parr_key]
            
            # Limpieza del código DEA / Plantel
            codigo_dea = clean_str(row.get('CODIGO PLANTEL')) or f"DEA_GEN_{idx+1}"
            nombre_plantel = clean_str(row.get('PLANTEL')) or "PLANTEL SIN NOMBRE"
            dependencia = standardize_dependencia(row.get('DEPENDENCIA'))
            
            # Coordenadas
            lat = row.get('LATITUD')
            long_val = row.get('LONGITUD')
            lat_float = float(lat) if pd.notna(lat) and isinstance(lat, (int, float)) else None
            long_float = float(long_val) if pd.notna(long_val) and isinstance(long_val, (int, float)) else None
            
            plantel_obj = Plantel(
                codigo_dea=codigo_dea,
                plantel=nombre_plantel,
                eponimo_anterior=clean_str(row.get('EPONIMO ANTERIOR')),
                dependencia=dependencia,
                denominacion=clean_str(row.get('DENOMINACIÓN')),
                direccion=clean_str(row.get('DIRECCIÓN DEL PLANTEL')),
                comunidad=clean_str(row.get('COMUNIDAD')),
                nombres_contacto=clean_str(row.get('NOMBRES Y APELLIDOS ')),
                ci_contacto=clean_str(row.get('CI')),
                telefono_contacto=clean_str(row.get('TLFN')),
                email_contacto=clean_str(row.get('CORREO ELECTRÓNICO ')),
                estatus_zona=clean_str(row.get('ESTATUS ZONA EDUC')) or "REGISTRADA EN ZONA",
                estatus_segen=clean_str(row.get('ESTATUS SEGEN')) or "NO LEVANTADO POR SEGEN",
                estatus_director=clean_str(row.get('ESTATUS DIRECTOR')) or "NO LEVANTADAS POR DIRECTOR",
                estatus_qr=clean_str(row.get('ESTATUS QR')) or "SIN QR ASIGNADO",
                qr_segen=clean_str(row.get('QR SEGEN')),
                qr_director=clean_str(row.get('QR DIRECTOR')),
                municipio_id=mun_id,
                parroquia_id=parr_id,
                municipio_nombre=mun_nom_clean,
                parroquia_nombre=parr_nom_clean,
                latitud=lat_float,
                longitud=long_float
            )
            db.add(plantel_obj)

        db.commit()
        print(f"✅ Se insertaron exitosamente {len(df)} planteles educativos.")

    # Crear Usuario Admin inicial si no existe
    admin_user = db.query(UsuarioAdmin).filter(UsuarioAdmin.username == "admin").first()
    if not admin_user:
        hashed_pwd = hash_password("admin123")
        admin_user = UsuarioAdmin(
            username="admin",
            hashed_password=hashed_pwd,
            nombre="Administrador Zona Educativa",
            email="admin@zonaeducativa.gob.ve"
        )
        db.add(admin_user)
        db.commit()
        print("✅ Usuario Administrador inicial creado: admin / admin123")

    # Sembrar algunas solicitudes de prueba iniciales para evaluar los KPIs del Dashboard
    if db.query(SolicitudQR).count() == 0:
        sample_planteles = db.query(Plantel).limit(10).all()
        roles_sample = ["DIRECTOR", "ENLACE_SEGEN", "SUPERVISOR", "DIRECTOR", "DIRECTOR"]
        tipos_sample = ["REPOSICION", "NUEVA_ASIGNACION", "CORRECCION", "REPOSICION", "NUEVA_ASIGNACION"]
        
        for idx, p in enumerate(sample_planteles[:5]):
            sol = SolicitudQR(
                plantel_id=p.id,
                tipo_solicitud=tipos_sample[idx],
                solicitante_rol=roles_sample[idx],
                solicitante_nombre=f"Solicitante {idx+1}",
                solicitante_ci=f"V-{12000000 + idx}",
                solicitante_telefono=f"0414-{1000000 + idx}",
                solicitante_email=f"solicitante{idx+1}@educacion.gob.ve",
                motivo="Solicitud enviada para actualización de código QR en plantel",
                estatus_solicitud="PENDIENTE"
            )
            db.add(sol)
        db.commit()
        print("✅ Se sembraron solicitudes de prueba para KPIs iniciales.")

    db.close()

if __name__ == "__main__":
    xlsm_path = os.getenv("XLSM_PATH", "/home/seem/Documentos/_proyectos/zona_educativa/PLANTELES EDUCATIVOS - copia.xlsm")
    seed_database(xlsm_path)
