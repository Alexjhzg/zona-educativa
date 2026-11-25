import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .database import Base, engine
    from .routers import admin_data, auth, dashboard, planteles, solicitudes
    from .services.cron_cleaner import start_cron_cleaner
except ImportError:
    from database import Base, engine
    from routers import admin_data, auth, dashboard, planteles, solicitudes
    from services.cron_cleaner import start_cron_cleaner

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zona Educativa - API de Solicitudes y Dashboard QR",
    description="API REST para recepción de solicitudes de QR de planteles educativos y agregación analítica de KPIs.",
    version="1.0.0",
)

# Configuración CORS restrictiva desde variable de entorno CORS_ORIGINS
_default_origins = (
    "http://localhost:5173,http://localhost:8080,http://127.0.0.1:5173,http://127.0.0.1:8080"
)
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Registrar Routers
app.include_router(planteles.router)
app.include_router(solicitudes.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(admin_data.router)


@app.on_event("startup")
def on_startup():
    try:
        start_cron_cleaner()
    except Exception as e:
        print(f"Error al iniciar cron cleaner: {e}")


@app.get("/api/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "service": "Zona Educativa QR API", "version": "1.0.0"}
