from app.main import ALLOWED_ORIGINS, app
from app.routers.admin_data import ALLOWED_COLUMNS
from app.routers.auth import SECRET_KEY
from fastapi.testclient import TestClient

client = TestClient(app)


def test_secret_key_not_hardcoded():
    assert SECRET_KEY
    assert SECRET_KEY != "zona_educativa_super_secret_jwt_key_2026"


def test_cors_origins_no_wildcard():
    assert "*" not in ALLOWED_ORIGINS
    assert len(ALLOWED_ORIGINS) > 0


def test_protected_endpoints_require_auth():
    assert client.get("/api/solicitudes").status_code == 401
    assert (
        client.patch("/api/solicitudes/1/estatus", json={"estatus": "PROCESADO"}).status_code == 401
    )
    assert client.get("/api/dashboard/kpis").status_code == 401
    assert client.get("/api/dashboard/solicitudes").status_code == 401


def test_admin_allowed_columns_exclude_primary_keys():
    for table_name, columns in ALLOWED_COLUMNS.items():
        assert "id" not in columns, f"'id' no debe ser editable en {table_name}"
