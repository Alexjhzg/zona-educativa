import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Si hay variable DATABASE_URL (Docker/Postgres), se usa; de lo contrario SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zona_educativa.db")

# Limpiar posibles saltos de línea o espacios accidentales de la variable de entorno
DATABASE_URL = DATABASE_URL.strip().replace("\n", "").replace("\r", "")

# Compatibilidad para SQLAlchemy cuando el URL inicia con postgres:// (Supabase / Heroku / Render)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URL = DATABASE_URL

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
