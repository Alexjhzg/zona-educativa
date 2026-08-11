import os
import json
import time
from app.database import SessionLocal
from app.services.backup_service import create_table_backup, cleanup_old_backups, BACKUP_DIR, ensure_backup_dir

def test_create_table_backup():
    """Verifica que se genere un archivo de respaldo estructurado con metadata y filas."""
    db = SessionLocal()
    try:
        backup_file = create_table_backup(db, "planteles")
        assert os.path.exists(backup_file)
        assert backup_file.endswith(".json")

        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "metadata" in data
        assert data["metadata"]["table_name"] == "planteles"
        assert "rows" in data
        assert isinstance(data["rows"], list)

        # Limpiar archivo generado por el test
        os.remove(backup_file)
    finally:
        db.close()

def test_cleanup_old_backups_retention():
    """Verifica que los archivos con antigüedad > 7 días sean purgados y los recientes preservados."""
    backup_dir = ensure_backup_dir()

    # 1. Crear un archivo falso "reciente" (hoy)
    recent_file = os.path.join(backup_dir, "backup_planteles_recent_test.json")
    with open(recent_file, "w") as f:
        f.write('{"test": "recent"}')

    # 2. Crear un archivo falso "obsoleto" (hace 8 días)
    old_file = os.path.join(backup_dir, "backup_planteles_old_test.json")
    with open(old_file, "w") as f:
        f.write('{"test": "old"}')

    # Alterar el mtime del archivo antiguo a hace 8 días (8 * 86400 + 100 segundos)
    eight_days_ago = time.time() - (8 * 86400 + 100)
    os.utime(old_file, (eight_days_ago, eight_days_ago))

    # 3. Ejecutar la purga con retención de 7 días
    deleted = cleanup_old_backups(max_days=7)

    # 4. Asertos
    assert old_file in deleted
    assert not os.path.exists(old_file)
    assert os.path.exists(recent_file)

    # Limpiar archivo reciente
    if os.path.exists(recent_file):
        os.remove(recent_file)
