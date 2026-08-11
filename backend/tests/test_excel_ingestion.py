import os
import io
import pandas as pd
from app.database import SessionLocal
from app.models import Plantel
from app.excel_importer import process_excel_import
from app.services.backup_service import create_table_backup

def test_excel_ingestion_and_backup():
    """Verifica que el respaldo automático y el Upsert de planteles funcionen correctamente."""
    db = SessionLocal()
    try:
        # 1. Ejecutar respaldo previo
        backup_file = create_table_backup(db, "planteles")
        assert os.path.exists(backup_file)

        # 2. Generar un archivo Excel sintético en memoria con un plantel modificado
        test_dea = "TEST_DEA_9999"
        df_test = pd.DataFrame([{
            "MUNICIPIO": "MATURIN",
            "PARROQUIA": "SAN SIMON",
            "CODIGO PLANTEL": test_dea,
            "PLANTEL": "U.E. PLANTEL TEST AUTOMATIZADO",
            "DEPENDENCIA": "ESTADAL",
            "DENOMINACIÓN": "UNIDAD EDUCATIVA",
            "DIRECCIÓN DEL PLANTEL": "AV. PRINCIPAL MATURIN",
            "COMUNIDAD": "CENTRO",
            "NOMBRES Y APELLIDOS ": "DIRECTOR PRUEBA",
            "CI": "V-12345678",
            "TLFN": "04141234567",
            "CORREO ELECTRÓNICO ": "test@zonaeducativa.gob.ve",
            "ESTATUS ZONA EDUC": "REGISTRADA EN ZONA",
            "ESTATUS SEGEN": "LEVANTADO POR SEGEN",
            "ESTATUS DIRECTOR": "LEVANTADAS POR DIRECTOR",
            "ESTATUS QR": "QR SEGEN Y DIRECTOR ACTIVOS",
            "LATITUD": 9.745,
            "LONGITUD": -63.185
        }])

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_test.to_excel(writer, sheet_name='planteles', index=False)
        excel_bytes = output.getvalue()

        # 3. Procesar ingesta del Excel sintético
        resultado = process_excel_import(excel_bytes, db)

        assert resultado["total_filas"] == 1
        assert resultado["errores"] == 0

        # 4. Verificar que el registro existe en la Base de Datos
        plantel_db = db.query(Plantel).filter(Plantel.codigo_dea == test_dea).first()
        assert plantel_db is not None
        assert plantel_db.plantel == "U.E. PLANTEL TEST AUTOMATIZADO"
        assert plantel_db.dependencia == "ESTADAL"

        # Limpiar registro de test y archivo de respaldo generado
        db.delete(plantel_db)
        db.commit()

        if os.path.exists(backup_file):
            os.remove(backup_file)

    finally:
        db.close()
