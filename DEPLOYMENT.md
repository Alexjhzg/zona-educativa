# 🐳 Guía de Despliegue - Zona Educativa

Este documento contiene las instrucciones detalladas para desplegar el proyecto **Zona Educativa** tanto en entornos de desarrollo local como en servidores de producción utilizando **Docker Compose** y **Nginx**.

---

## 🛠️ Prerrequisitos del Sistema

Asegúrate de contar con los siguientes elementos instalados en el servidor o máquina local:

- **Docker Engine**: versión 20.10.0 o superior.
- **Docker Compose**: versión 2.0.0 o superior.
- **Git**: para la clonación del código fuente.

---

## ⚙️ Variables de Entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto basándote en la plantilla `.env.example`:

```env
# Configuración Base de Datos PostgreSQL
POSTGRES_USER=zona_user
POSTGRES_PASSWORD=zona_pass_2026
POSTGRES_DB=zona_educativa_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Configuración Backend FastAPI
SECRET_KEY=super_secret_jwt_key_zona_educativa_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Ruta del archivo Excel fuente para ETL
XLSM_PATH=/app/PLANTELES EDUCATIVOS - copia.xlsm
```

---

## 🚀 Despliegue con Docker Compose

El proyecto está orquestado en 3 contenedores principales:
1. `zona_educativa_db`: Base de datos PostgreSQL 16 Alpine.
2. `zona_educativa_backend`: API REST en FastAPI.
3. `zona_educativa_frontend`: Servidor Nginx que sirve la SPA compilada en Vue 3.

### Pasos de Ejecución:

1. **Construir e Iniciar Contenedores**:
   ```bash
   docker-compose up -d --build
   ```

2. **Verificar que los servicios estén activos**:
   ```bash
   docker-compose ps
   ```

3. **Inspeccionar Logs en caso de algún problema**:
   ```bash
   # Logs de todos los servicios
   docker-compose logs -f

   # Logs específicos del backend
   docker-compose logs -f backend
   ```

4. **Ejecutar Seeding de Datos Manualmente (Si fuera necesario)**:
   ```bash
   docker-compose exec backend python app/seed_data.py
   ```

---

## 🌐 Configuración del Proxy Inverso (Nginx)

El frontend incluye su propio archivo `nginx.conf` optimizado para SPAs en Vue Router (`history mode`):

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🛡️ Mantenimiento y Reinicio

- **Detener los servicios sin borrar datos**:
  ```bash
  docker-compose stop
  ```

- **Reiniciar servicios**:
  ```bash
  docker-compose restart
  ```

- **Eliminar contenedores y volúmenes (Reiniciar base de datos de cero)**:
  ```bash
  docker-compose down -v
  ```
