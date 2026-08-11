from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .database import engine, Base
    from .routers import planteles, solicitudes, auth, dashboard, admin_data
    from .services.cron_cleaner import start_cron_cleaner
except ImportError:
    from database import engine, Base
    from routers import planteles, solicitudes, auth, dashboard, admin_data
    from services.cron_cleaner import start_cron_cleaner

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zona Educativa - API de Solicitudes y Dashboard QR",
    description="API REST para recepción de solicitudes de QR de planteles educativos y agregación analítica de KPIs.",
    version="1.0.0"
)

# Configuración CORS para permitir conexiones desde el Frontend Vue 3
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
