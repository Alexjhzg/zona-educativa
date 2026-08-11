import os
import bcrypt
import pandas as pd
from database import engine, SessionLocal, Base
from models import Municipio, Parroquia, Plantel, SolicitudQR, UsuarioAdmin

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
            if mun_nom not in municipios_map:
                mun_obj = db.query(Municipio).filter(Municipio.nombre == mun_nom).first()
                if not mun_obj:
                    mun_obj = Municipio(nombre=mun_nom)
                    db.add(mun_obj)
                    db.commit()
                    db.refresh(mun_obj)
                municipios_map[mun_nom] = mun_obj
            mun_obj = municipios_map[mun_nom]
            
            # Crear o buscar Parroquia
            parr_key = f"{mun_nom}_{parr_nom}"
            if parr_key not in parroquias_map:
                parr_obj = db.query(Parroquia).filter(
                    Parroquia.municipio_id == mun_obj.id,
                    Parroquia.nombre == parr_nom
                ).first()
                if not parr_obj:
                    parr_obj = Parroquia(municipio_id=mun_obj.id, nombre=parr_nom)
                    db.add(parr_obj)
                    db.commit()
                    db.refresh(parr_obj)
                parroquias_map[parr_key] = parr_obj
            parr_obj = parroquias_map[parr_key]
            
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
                municipio_id=mun_obj.id,
                parroquia_id=parr_obj.id,
                municipio_nombre=mun_nom,
                parroquia_nombre=parr_nom,
                latitud=lat_float,
                longitud=long_float
            )
            planteles_to_insert.append(plantel_obj)
        
        db.bulk_save_objects(planteles_to_insert)
        db.commit()
        print(f"✅ Se insertaron exitosamente {len(planteles_to_insert)} planteles educativos.")

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
