import threading
import time
from datetime import datetime
from .backup_service import cleanup_old_backups

_scheduler_thread = None
_stop_event = threading.Event()

def run_backup_cleanup_loop(interval_seconds: int = 86400):
    """Bucle en segundo plano que ejecuta la purga de respaldos obsoletos."""
    print("⏰ [Cron Job] Iniciado servicio de purga de respaldos (Retención: 7 Días).")
    while not _stop_event.is_set():
        try:
            deleted = cleanup_old_backups(max_days=7)
            if deleted:
                print(f"🧹 [Cron Job] Purga completada: {len(deleted)} respaldos obsoletos eliminados.")
            else:
                print("✅ [Cron Job] Chequeo de respaldos completado: Ningún archivo excede los 7 días.")
        except Exception as e:
            print(f"⚠️ [Cron Job] Error al purgar respaldos: {e}")

        # Esperar interval_seconds o interrumpir si se solicita apagar
        _stop_event.wait(timeout=interval_seconds)

def start_cron_cleaner(interval_seconds: int = 86400):
    """Inicia el hilo del cron job si no se encuentra activo."""
    global _scheduler_thread
    if _scheduler_thread is None or not _scheduler_thread.is_alive():
        _stop_event.clear()
        _scheduler_thread = threading.Thread(target=run_backup_cleanup_loop, args=(interval_seconds,), daemon=True)
        _scheduler_thread.start()

def stop_cron_cleaner():
    """Detiene el hilo del cron job de forma segura."""
    _stop_event.set()
