import sys
import os
import io
import pytest
import pandas as pd
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from main import app

client = TestClient(app)

def get_admin_token():
    login_data = {"username": "admin", "password": "admin123"}
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

def test_import_excel_unauthorized():
    files = {"file": ("test.xlsx", b"dummy content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = client.post("/api/admin/data/import-excel", files=files)
    assert response.status_code == 401

def test_import_excel_invalid_extension():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": ("test.txt", b"dummy content", "text/plain")}
    response = client.post("/api/admin/data/import-excel", headers=headers, files=files)
    assert response.status_code == 400
    assert "Formato de archivo no válido" in response.json()["detail"]

def test_import_excel_success():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Crear DataFrame sintético de prueba
    df_data = {
        "MUNICIPIO": ["MATURIN", "MATURIN"],
        "PARROQUIA": ["ALTO DE LOS GODOS", "BOQUERON"],
        "CODIGO PLANTEL": ["OD00001TEST", "OD00002TEST"],
        "PLANTEL": ["ESCUELA PRUEBA IMPORT 1", "ESCUELA PRUEBA IMPORT 2"],
        "EPONIMO ANTERIOR": [None, "VIEJO NOMBRE"],
        "DEPENDENCIA": ["NACIONAL", "ESTADAL"],
        "DENOMINACIÓN": ["U.E.", "E.B."],
        "DIRECCIÓN DEL PLANTEL": ["Calle 1", "Calle 2"],
        "COMUNIDAD": ["Comunidad A", "Comunidad B"],
        "NOMBRES Y APELLIDOS ": ["Juan Perez", "Maria Gomez"],
        "CI": ["V-10000001", "V-10000002"],
        "TLFN": ["0414-1111111", "0414-2222222"],
        "CORREO ELECTRÓNICO ": ["juan@test.com", "maria@test.com"],
        "ESTATUS ZONA EDUC": ["REGISTRADA EN ZONA", "REGISTRADA EN ZONA"],
        "ESTATUS SEGEN": ["NO LEVANTADO POR SEGEN", "NO LEVANTADO POR SEGEN"],
        "ESTATUS DIRECTOR": ["NO LEVANTADAS POR DIRECTOR", "NO LEVANTADAS POR DIRECTOR"],
        "ESTATUS QR": ["SIN QR ASIGNADO", "SIN QR ASIGNADO"],
        "QR SEGEN": [None, None],
        "QR DIRECTOR": [None, None],
        "LATITUD": [9.74, 9.75],
        "LONGITUD": [-63.18, -63.19]
    }
    df = pd.DataFrame(df_data)

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='planteles', index=False)
    excel_bytes = excel_buffer.getvalue()

    files = {"file": ("planteles_test.xlsx", excel_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = client.post("/api/admin/data/import-excel", headers=headers, files=files)
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["message"] == "Importación completada exitosamente"
    detalles = res_data["detalles"]
    assert detalles["total_filas"] == 2
    assert (detalles["creados"] + detalles["actualizados"]) == 2
    assert detalles["errores"] == 0
