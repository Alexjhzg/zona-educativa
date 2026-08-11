import io
import pandas as pd
from typing import Dict, Any
from sqlalchemy.orm import Session

try:
    from .models import Municipio, Parroquia, Plantel
except (ImportError, ModuleNotFoundError):
    try:
        from models import Municipio, Parroquia, Plantel
    except (ImportError, ModuleNotFoundError):
        from app.models import Municipio, Parroquia, Plantel

def clean_str(val) -> str | None:
    if pd.isna(val) or val is None:
        return None
    val_str = str(val).strip()
    return val_str if val_str else None

def standardize_dependencia(val) -> str:
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

REQUIRED_COLUMNS = ['CODIGO PLANTEL', 'PLANTEL', 'MUNICIPIO']

OFFICIAL_COLUMNS_PLANTELES = [
    'MUNICIPIO', 'PARROQUIA', 'CODIGO PLANTEL', 'PLANTEL', 'EPONIMO ANTERIOR',
    'DEPENDENCIA', 'DENOMINACIÓN', 'DIRECCIÓN DEL PLANTEL', 'COMUNIDAD',
    'NOMBRES Y APELLIDOS ', 'CI', 'TLFN', 'CORREO ELECTRÓNICO ',
    'ESTATUS ZONA EDUC', 'ESTATUS SEGEN', 'ESTATUS DIRECTOR', 'ESTATUS QR',
    'QR SEGEN', 'QR DIRECTOR', 'QR DIRECTOR SEP', 'QR DIRECTOR JUL 2026',
    'RIF', 'SEGMENTO', 'MANZANA', 'SECTOR', 'CENTRO POBLADO', 'TIPOLOGIA', 'UBICACIÓN',
    'LATITUD', 'LONGITUD', 'ALTITUD', 'PRECISION', 'http://CedulaInmobiliaria.ve/'
]

def validate_excel_schema(df: pd.DataFrame):
    """Verifica que el DataFrame contenga las columnas obligatorias del esquema oficial."""
    columns_upper = [str(col).strip().upper() for col in df.columns]
    missing = []
    for req in REQUIRED_COLUMNS:
        if not any(req in col for col in columns_upper):
            missing.append(req)
    if missing:
        raise ValueError(
            f"Esquema de Excel inválido. Faltan las columnas obligatorias: {', '.join(missing)}. "
            f"Por favor utilice la plantilla oficial para garantizar el orden de columnas y tipos de datos."
        )

def generate_excel_template(table_name: str = "planteles") -> bytes:
    """Genera un archivo Excel (.xlsx) formateado con los encabezados oficiales y filas sintéticas de ejemplo con sentido."""
    df_template = pd.DataFrame(columns=OFFICIAL_COLUMNS_PLANTELES)
    
    example_rows = [
        {
            'MUNICIPIO': 'MATURÍN',
            'PARROQUIA': 'SAN SIMÓN',
            'CODIGO PLANTEL': 'DEA_EJEMPLO_001',
            'PLANTEL': 'U.E. DE EJEMPLO SIMÓN BOLÍVAR',
            'EPONIMO ANTERIOR': 'SIMÓN BOLÍVAR (EJEMPLO)',
            'DEPENDENCIA': 'ESTADAL',
            'DENOMINACIÓN': 'UNIDAD EDUCATIVA',
            'DIRECCIÓN DEL PLANTEL': 'AV. PRINCIPAL DE EJEMPLO, SECTOR CENTRO',
            'COMUNIDAD': 'COMUNIDAD EJEMPLO 1',
            'NOMBRES Y APELLIDOS ': 'EJEMPLO JUAN PÉREZ',
            'CI': 'V-00000001',
            'TLFN': '04140000001',
            'CORREO ELECTRÓNICO ': 'ejemplo.director@zonaeducativa.gob.ve',
            'ESTATUS ZONA EDUC': 'REGISTRADA EN ZONA',
            'ESTATUS SEGEN': 'LEVANTADO POR SEGEN',
            'ESTATUS DIRECTOR': 'LEVANTADAS POR DIRECTOR',
            'ESTATUS QR': 'QR SEGEN',
            'LATITUD': 9.745000,
            'LONGITUD': -63.185000
        },
        {
            'MUNICIPIO': 'CARIPE',
            'PARROQUIA': 'CARIPE',
            'CODIGO PLANTEL': 'DEA_EJEMPLO_002',
            'PLANTEL': 'LICEO NACIONAL DE EJEMPLO ANDRÉS ELOY BLANCO',
            'EPONIMO ANTERIOR': 'ANDRÉS ELOY (EJEMPLO)',
            'DEPENDENCIA': 'NACIONAL',
            'DENOMINACIÓN': 'LICEO BOLIVARIANO',
            'DIRECCIÓN DEL PLANTEL': 'CALLE 2 DE EJEMPLO, SECTOR LAS FLORES',
            'COMUNIDAD': 'COMUNIDAD EJEMPLO 2',
            'NOMBRES Y APELLIDOS ': 'EJEMPLO MARÍA RODRÍGUEZ',
            'CI': 'V-00000002',
            'TLFN': '04160000002',
            'CORREO ELECTRÓNICO ': 'ejemplo.liceo@zonaeducativa.gob.ve',
            'ESTATUS ZONA EDUC': 'REGISTRADA EN ZONA',
            'ESTATUS SEGEN': 'NO LEVANTADO POR SEGEN',
            'ESTATUS DIRECTOR': 'NO LEVANTADAS POR DIRECTOR',
            'ESTATUS QR': 'SIN QR ASIGNADO',
            'LATITUD': 10.170000,
            'LONGITUD': -63.480000
        }
    ]
    df_template = pd.concat([df_template, pd.DataFrame(example_rows)], ignore_index=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_template.to_excel(writer, sheet_name='planteles', index=False)
    return output.getvalue()

def process_excel_import(file_bytes: bytes, db: Session) -> Dict[str, Any]:
    """
    Procesa un archivo Excel (.xlsx / .xlsm) y realiza un upsert de planteles en la BD.
    Retorna métricas del proceso.
    """
    excel_file = io.BytesIO(file_bytes)
    
    # Intentar leer la hoja 'planteles', o tomar la primera hoja disponible
    xl = pd.ExcelFile(excel_file)
    sheet_name = 'planteles' if 'planteles' in xl.sheet_names else xl.sheet_names[0]
    
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    validate_excel_schema(df)
    total_filas = len(df)
    
    # Mapeo en memoria de Municipios y Parroquias para optimizar consultas
    municipios_db = db.query(Municipio).all()
    municipios_map = {m.nombre.upper(): m for m in municipios_db}
    
    parroquias_db = db.query(Parroquia).all()
    parroquias_map = {f"{p.municipio_id}_{p.nombre.upper()}": p for p in parroquias_db}

    # Cargar planteles existentes mapeados por codigo_dea
    existing_planteles = {p.codigo_dea: p for p in db.query(Plantel).all() if p.codigo_dea}

    creados = 0
    actualizados = 0
    errores = 0
    detalles_errores = []

    for idx, row in df.iterrows():
        try:
            mun_nom = (clean_str(row.get('MUNICIPIO')) or "MATURIN").upper()
            parr_nom = (clean_str(row.get('PARROQUIA')) or "SIN PARROQUIA").upper()

            # Buscar o crear Municipio
            if mun_nom not in municipios_map:
                mun_obj = db.query(Municipio).filter(Municipio.nombre == mun_nom).first()
                if not mun_obj:
                    mun_obj = Municipio(nombre=mun_nom)
                    db.add(mun_obj)
                    db.commit()
                    db.refresh(mun_obj)
                municipios_map[mun_nom] = mun_obj
            mun_obj = municipios_map[mun_nom]

            # Buscar o crear Parroquia
            parr_key = f"{mun_obj.id}_{parr_nom}"
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

            # Datos del Plantel
            codigo_dea = clean_str(row.get('CODIGO PLANTEL')) or f"DEA_GEN_{idx+1}"
            nombre_plantel = clean_str(row.get('PLANTEL')) or "PLANTEL SIN NOMBRE"
            dependencia = standardize_dependencia(row.get('DEPENDENCIA'))

            def parse_float(val):
                if pd.notna(val):
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return None
                return None

            datos = {
                "codigo_dea": codigo_dea,
                "plantel": nombre_plantel,
                "eponimo_anterior": clean_str(row.get('EPONIMO ANTERIOR')),
                "dependencia": dependencia,
                "denominacion": clean_str(row.get('DENOMINACIÓN')),
                "direccion": clean_str(row.get('DIRECCIÓN DEL PLANTEL')),
                "comunidad": clean_str(row.get('COMUNIDAD')),
                "nombres_contacto": clean_str(row.get('NOMBRES Y APELLIDOS ')),
                "ci_contacto": clean_str(row.get('CI')),
                "telefono_contacto": clean_str(row.get('TLFN')),
                "email_contacto": clean_str(row.get('CORREO ELECTRÓNICO ')),
                "estatus_zona": clean_str(row.get('ESTATUS ZONA EDUC')) or "REGISTRADA EN ZONA",
                "estatus_segen": clean_str(row.get('ESTATUS SEGEN')) or "NO LEVANTADO POR SEGEN",
                "estatus_director": clean_str(row.get('ESTATUS DIRECTOR')) or "NO LEVANTADAS POR DIRECTOR",
                "estatus_qr": clean_str(row.get('ESTATUS QR')) or "SIN QR ASIGNADO",
                "qr_segen": clean_str(row.get('QR SEGEN')),
                "qr_director": clean_str(row.get('QR DIRECTOR')),
                "qr_director_sep": clean_str(row.get('QR DIRECTOR SEP')),
                "qr_director_jul_2026": clean_str(row.get('QR DIRECTOR JUL 2026')),
                "rif": clean_str(row.get('RIF')),
                "segmento": clean_str(row.get('SEGMENTO')),
                "manzana": clean_str(row.get('MANZANA')),
                "sector": clean_str(row.get('SECTOR')),
                "centro_poblado": clean_str(row.get('CENTRO POBLADO')),
                "tipologia": clean_str(row.get('TIPOLOGIA')),
                "ubicacion": clean_str(row.get('UBICACIÓN')),
                "municipio_id": mun_obj.id,
                "parroquia_id": parr_obj.id,
                "municipio_nombre": mun_nom,
                "parroquia_nombre": parr_nom,
                "latitud": parse_float(row.get('LATITUD')),
                "longitud": parse_float(row.get('LONGITUD')),
                "altitud": parse_float(row.get('ALTITUD')),
                "precision_gps": parse_float(row.get('PRECISION')),
                "cedula_inmobiliaria_url": clean_str(row.get('http://CedulaInmobiliaria.ve/'))
            }

            if codigo_dea in existing_planteles:
                # Actualizar plantel existente
                plantel_existente = existing_planteles[codigo_dea]
                for field, value in datos.items():
                    setattr(plantel_existente, field, value)
                actualizados += 1
            else:
                # Insertar nuevo plantel
                nuevo_plantel = Plantel(**datos)
                db.add(nuevo_plantel)
                existing_planteles[codigo_dea] = nuevo_plantel
                creados += 1

        except Exception as e:
            errores += 1
            detalles_errores.append(f"Fila {idx + 2}: {str(e)}")

    db.commit()

    return {
        "total_filas": total_filas,
        "creados": creados,
        "actualizados": actualizados,
        "errores": errores,
        "detalles_errores": detalles_errores[:10]  # Limitar muestra de errores
    }
