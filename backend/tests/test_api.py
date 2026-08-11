import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_search_planteles():
    response = client.get("/api/planteles/search?q=MATURIN")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_crear_solicitud_qr():
    # Buscar un plantel válido
    search_res = client.get("/api/planteles/search?q=MATURIN")
    plantel_id = search_res.json()[0]["id"]

    payload = {
        "plantel_id": plantel_id,
        "tipo_solicitud": "REPOSICION",
        "solicitante_rol": "DIRECTOR",
        "solicitante_nombre": "Director Prueba QA",
        "solicitante_ci": "V-12345678",
        "solicitante_telefono": "0412-5555555",
        "solicitante_email": "director.qa@educacion.gob.ve",
        "motivo": "Código QR deteriorado por intemperie"
    }

    response = client.post("/api/solicitudes", json=payload)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["solicitante_nombre"] == "Director Prueba QA"
    assert res_data["estatus_solicitud"] == "PENDIENTE"

def test_kpis_dashboard():
    response = client.get("/api/dashboard/kpis")
    assert response.status_code == 200
    kpis = response.json()
    assert kpis["total_planteles"] >= 988
    assert "ranking_roles" in kpis
    assert len(kpis["ranking_roles"]) > 0
    assert kpis["top_solicitante_rol"] is not None

def test_auth_login_admin():
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Probar endpoint protegido sin token -> 401
    resp_unauth = client.get("/api/dashboard/solicitudes")
    assert resp_unauth.status_code == 401

    # Probar endpoint protegido con token -> 200
    headers = {"Authorization": f"Bearer {token}"}
    resp_auth = client.get("/api/dashboard/solicitudes", headers=headers)
    assert resp_auth.status_code == 200
    assert isinstance(resp_auth.json(), list)
