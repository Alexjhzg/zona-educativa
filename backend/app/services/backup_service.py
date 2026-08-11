import os
import json
import time
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

# Directorio base para almacenar respaldos temporales
BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "backups")

def ensure_backup_dir() -> str:
    """Garantiza que el directorio de respaldos exista."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR, exist_ok=True)
    return BACKUP_DIR

def create_table_backup(db: Session, table_name: str) -> str:
    """
    Crea un respaldo estructurado en JSON/SQL de una tabla específica antes de una ingesta.
    Retorna la ruta absoluta del archivo de respaldo generado.
    """
    backup_path = ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{table_name}_{timestamp}.json"
    full_path = os.path.join(backup_path, filename)

    # Sanitizar nombre de tabla para SQL raw
    allowed_tables = ["planteles", "solicitudes_qr", "municipios"]
    if table_name not in allowed_tables:
        raise ValueError(f"Tabla '{table_name}' no permitida para respaldos.")

    # Consultar todos los datos actuales
    result = db.execute(text(f"SELECT * FROM {table_name}")).mappings().all()
    rows_data = [dict(row) for row in result]

    # Convertir tipos no serializables a string
    for row in rows_data:
        for k, v in row.items():
            if isinstance(v, (datetime, date)):
                row[k] = v.isoformat()

    backup_content = {
        "metadata": {
            "table_name": table_name,
            "created_at": datetime.now().isoformat(),
            "total_rows": len(rows_data)
        },
        "rows": rows_data
    }

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(backup_content, f, ensure_ascii=False, indent=2)

    return full_path

def cleanup_old_backups(max_days: int = 7) -> List[str]:
    """
    Escanea la carpeta de respaldos y elimina cualquier archivo con antigüedad mayor a max_days.
    Retorna la lista de rutas de archivos eliminados.
    """
    backup_dir = ensure_backup_dir()
    deleted_files = []
    cutoff_time = time.time() - (max_days * 86400)  # 86400 segundos por día

    for filename in os.listdir(backup_dir):
        if filename.startswith("backup_") and filename.endswith(".json"):
            file_path = os.path.join(backup_dir, filename)
            try:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    os.remove(file_path)
                    deleted_files.append(file_path)
            except Exception as e:
                print(f"Error al verificar/eliminar respaldo {filename}: {e}")

    return deleted_files
