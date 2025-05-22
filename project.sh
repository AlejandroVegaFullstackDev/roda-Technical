#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────────
# Script de inicialización de la arquitectura de carpetas
# para el microservicio “e-Bike Autolock” (Clean Architecture)
# ────────────────────────────────────────────────────────────────
# Ejecución (vía SSH o local):
#   chmod +x project.sh && ./project.sh
# ────────────────────────────────────────────────────────────────

set -e

# Carpeta raíz del proyecto
PROJECT_ROOT="autolock_microservice"
mkdir -p "$PROJECT_ROOT"

# ─────────── Archivos raíz ───────────
touch "$PROJECT_ROOT"/{README.md,requirements.txt,Dockerfile,docker-compose.yml,.env.example,pyproject.toml}

# ─────────── Estructura src/ (Clean Architecture) ───────────
mkdir -p "$PROJECT_ROOT"/src/{domain,usecases,interfaces/{api,device},infrastructure/{db,repositories,services},config}

# Paquetes Python
touch "$PROJECT_ROOT"/src/{__init__.py,main.py}
touch "$PROJECT_ROOT"/src/config/{__init__.py,settings.py}

# Dominio
touch "$PROJECT_ROOT"/src/domain/{__init__.py,bike.py,user.py,event.py,enums.py,repositories.py}

# Casos de uso
touch "$PROJECT_ROOT"/src/usecases/{__init__.py,immobilize_bike_service.py,event_scheduler.py}

# Interfaces - API (Flask Blueprints) y dispositivo simulado
touch "$PROJECT_ROOT"/src/interfaces/api/{__init__.py,auth_blueprint.py,bikes_blueprint.py,events_blueprint.py}
touch "$PROJECT_ROOT"/src/interfaces/device/{__init__.py,gps_service_stub.py}

# Infraestructura - DB + repositorios + servicios externos
touch "$PROJECT_ROOT"/src/infrastructure/db/{__init__.py,base.py,models.py}
touch "$PROJECT_ROOT"/src/infrastructure/repositories/{__init__.py,bike_repository_sqlalchemy.py,event_repository_sqlalchemy.py,user_repository_sqlalchemy.py}
touch "$PROJECT_ROOT"/src/infrastructure/services/{__init__.py,gps_client_http.py}

# ─────────── Migraciones y tests ───────────
mkdir -p "$PROJECT_ROOT"/{migrations,tests/{domain,usecases,interfaces}}
touch "$PROJECT_ROOT"/tests/{__init__.py}
touch "$PROJECT_ROOT"/tests/domain/test_bike.py
touch "$PROJECT_ROOT"/tests/usecases/test_immobilize_bike_service.py
touch "$PROJECT_ROOT"/tests/interfaces/test_api.py

echo "✔️  Arquitectura de carpetas creada en ./$PROJECT_ROOT"

