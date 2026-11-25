# Modelo de Base de Datos — Zona Educativa

Este documento refleja el esquema relacional real definido en [`backend/app/models.py`](../backend/app/models.py) con SQLAlchemy 2.0.

- **Motor en producción / Docker:** PostgreSQL 16 (`DATABASE_URL`)
- **Motor en desarrollo local / fallback:** SQLite (`sqlite:///./zona_educativa.db`)
- **Creación de tablas:** `Base.metadata.create_all(bind=engine)` en `backend/app/main.py`

---

## 1. Diagrama Entidad-Relación (ERD)

```mermaid
erDiagram
    MUNICIPIOS ||--o{ PARROQUIAS : "municipio_id"
    MUNICIPIOS ||--o{ PLANTELES : "municipio_id"
    PARROQUIAS ||--o{ PLANTELES : "parroquia_id"
    PLANTELES ||--o{ SOLICITUDES_QR : "plantel_id"

    MUNICIPIOS {
        int id PK
        varchar_100 nombre UK
    }

    PARROQUIAS {
        int id PK
        int municipio_id FK
        varchar_100 nombre
    }

    PLANTELES {
        int id PK
        varchar_50 codigo_dea UK
        varchar_255 plantel
        varchar_255 eponimo_anterior
        varchar_100 dependencia
        varchar_100 denominacion
        text direccion
        varchar_150 comunidad
        varchar_200 nombres_contacto
        varchar_50 ci_contacto
        varchar_50 telefono_contacto
        varchar_150 email_contacto
        varchar_100 estatus_zona
        varchar_100 estatus_segen
        varchar_100 estatus_director
        varchar_100 estatus_qr
        varchar_100 qr_segen
        varchar_100 qr_director
        varchar_100 qr_director_sep
        varchar_100 qr_director_jul_2026
        int municipio_id FK
        int parroquia_id FK
        varchar_100 municipio_nombre
        varchar_100 parroquia_nombre
        varchar_50 rif
        varchar_100 segmento
        varchar_100 manzana
        varchar_150 sector
        varchar_150 centro_poblado
        varchar_100 tipologia
        varchar_255 ubicacion
        float latitud
        float longitud
        float altitud
        float precision_gps
        varchar_255 cedula_inmobiliaria_url
    }

    SOLICITUDES_QR {
        int id PK
        int plantel_id FK
        varchar_50 tipo_solicitud
        varchar_50 solicitante_rol
        varchar_200 solicitante_nombre
        varchar_50 solicitante_ci
        varchar_50 solicitante_telefono
        varchar_150 solicitante_email
        text motivo
        varchar_50 estatus_solicitud
        datetime fecha_solicitud
    }

    USUARIOS_ADMIN {
        int id PK
        varchar_50 username UK
        varchar_255 hashed_password
        varchar_150 nombre
        varchar_150 email UK
        int activo
    }
```

---

## 2. Diccionario de Tablas

### 2.1 `municipios` (`Municipio`)
| Columna | Tipo | Restricciones | Índice |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | Sí |
| `nombre` | `String(100)` | `UNIQUE`, `NOT NULL` | Sí |

### 2.2 `parroquias` (`Parroquia`)
| Columna | Tipo | Restricciones | Índice |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | Sí |
| `municipio_id` | `Integer` | `FK -> municipios.id`, `NOT NULL` | No |
| `nombre` | `String(100)` | `NOT NULL` | Sí |

### 2.3 `planteles` (`Plantel`)
| Grupo | Columnas Clave | Restricciones / Notas |
| :--- | :--- | :--- |
| **Identificación** | `id` (PK), `codigo_dea` (`String(50)`, `UNIQUE`, `NOT NULL`, index), `plantel` (`String(255)`, `NOT NULL`, index), `eponimo_anterior` | `codigo_dea` es la clave de negocio usada para búsquedas y upsert en ETL. |
| **Clasificación** | `dependencia` (`String(100)`, `NOT NULL`, index), `denominacion`, `direccion` (`Text`), `comunidad` | `dependencia` agrupa Nacional, Estadal, Privada, etc. |
| **Contacto** | `nombres_contacto`, `ci_contacto`, `telefono_contacto`, `email_contacto` | Usados en búsqueda pública y contacto de dirección. |
| **Estatus** | `estatus_zona`, `estatus_segen` (index), `estatus_director` (index), `estatus_qr` (`NOT NULL`, index) | Valores principales de `estatus_qr`: `QR SEGEN`, `SIN QR ASIGNADO`, `REPONER QR`. |
| **Códigos QR** | `qr_segen`, `qr_director`, `qr_director_sep`, `qr_director_jul_2026` | Códigos históricos y vigentes asociados al plantel. |
| **Ubicación** | `municipio_id` (FK), `parroquia_id` (FK), `municipio_nombre` (index), `parroquia_nombre` | Desnormalización controlada de nombres para consultas rápidas. |
| **Territorio y GPS** | `rif`, `segmento`, `manzana`, `sector`, `centro_poblado`, `tipologia`, `ubicacion`, `latitud`, `longitud`, `altitud`, `precision_gps`, `cedula_inmobiliaria_url` | Datos georreferenciados e inmobiliarios del plantel. |

### 2.4 `solicitudes_qr` (`SolicitudQR`)
| Columna | Tipo | Restricciones / Default | Índice |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | Sí |
| `plantel_id` | `Integer` | `FK -> planteles.id`, `NOT NULL` | No |
| `tipo_solicitud` | `String(50)` | `NOT NULL` (`NUEVA_ASIGNACION`, `REPOSICION`, `CORRECCION`) | Sí |
| `solicitante_rol` | `String(50)` | `NOT NULL` (`DIRECTOR`, `ENLACE_SEGEN`, `SUPERVISOR`, `REPRESENTANTE`) | Sí |
| `solicitante_nombre` | `String(200)` | `NOT NULL` | No |
| `solicitante_ci` | `String(50)` | `NOT NULL` | No |
| `solicitante_telefono` | `String(50)` | `NOT NULL` | No |
| `solicitante_email` | `String(150)` | `NOT NULL` | No |
| `motivo` | `Text` | Nullable | No |
| `estatus_solicitud` | `String(50)` | Default `"PENDIENTE"` | Sí |
| `fecha_solicitud` | `DateTime` | Default `datetime.utcnow` | Sí |

### 2.5 `usuarios_admin` (`UsuarioAdmin`)
| Columna | Tipo | Restricciones / Default | Índice |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `PK` | Sí |
| `username` | `String(50)` | `UNIQUE`, `NOT NULL` | Sí |
| `hashed_password` | `String(255)` | `NOT NULL` (hash `bcrypt`) | No |
| `nombre` | `String(150)` | `NOT NULL` | No |
| `email` | `String(150)` | `UNIQUE`, `NOT NULL` | No |
| `activo` | `Integer` | Default `1` (`1` activo, `0` inactivo) | No |

