import os
import shutil
import tempfile

import bcrypt
import pytest

_TEST_TMP_DIR = tempfile.mkdtemp(prefix="zona_educativa_pytest_")
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_TEST_TMP_DIR, 'test_zona_educativa.db')}"
os.environ["BACKUP_DIR"] = os.path.join(_TEST_TMP_DIR, "backups")

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import Municipio, Parroquia, Plantel, UsuarioAdmin  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Crea el esquema y siembra datos mínimos aislados para toda la suite."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(UsuarioAdmin).filter(UsuarioAdmin.username == "admin").first():
            hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode("utf-8")
            db.add(
                UsuarioAdmin(
                    username="admin",
                    hashed_password=hashed,
                    nombre="Administrador QA",
                    email="admin@zonaeducativa.gob.ve",
                    activo=1,
                )
            )

        municipio = db.query(Municipio).filter(Municipio.nombre == "MATURIN").first()
        if not municipio:
            municipio = Municipio(nombre="MATURIN")
            db.add(municipio)
            db.flush()

        parroquia = db.query(Parroquia).filter(Parroquia.nombre == "SAN SIMON").first()
        if not parroquia:
            parroquia = Parroquia(municipio_id=municipio.id, nombre="SAN SIMON")
            db.add(parroquia)
            db.flush()

        if not db.query(Plantel).filter(Plantel.codigo_dea == "OD00010101").first():
            db.add(
                Plantel(
                    codigo_dea="OD00010101",
                    plantel="U.E. PRUEBA MATURIN",
                    dependencia="NACIONAL",
                    denominacion="UNIDAD EDUCATIVA",
                    municipio_id=municipio.id,
                    parroquia_id=parroquia.id,
                    municipio_nombre="MATURIN",
                    parroquia_nombre="SAN SIMON",
                    nombres_contacto="DIRECTOR BASE",
                    ci_contacto="V-12345678",
                    estatus_qr="QR SEGEN",
                )
            )
        db.commit()
    finally:
        db.close()

    yield

    engine.dispose()
    shutil.rmtree(_TEST_TMP_DIR, ignore_errors=True)
