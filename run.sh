#!/bin/bash

echo "📋 Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# 🆕 Crear .env si no existe
if [ ! -f .env ]; then
  echo "🆕 Creando archivo .env predeterminado..."
  cat <<EOF > .env
DB_USER=postgres
DB_PASSWORD=roda724
DB_NAME=roda_db
DB_HOST=postgres-db
DB_PORT=5432

JWT_SECRET_KEY=supersecretjwtkey
JWT_ACCESS_TOKEN_EXPIRES=3600

FLASK_ENV=development
EOF
fi

echo "🚀 Exportando variables de entorno..."
set -a
# Solo exportar líneas válidas
grep -v '^#' .env | grep -E '^[A-Za-z_][A-Za-z0-9_]*=' > .env.cleaned
source .env.cleaned
set +a
export PYTHONPATH=src

# # ⏳ Esperar a que PostgreSQL esté disponible (versión simplificada)
# echo "⏳ Esperando 10 segundos a que PostgreSQL inicie..."
# sleep 10

# ⚙️ Ejecutar migraciones
# echo "🔧 Ejecutando migraciones..."
# export FLASK_APP=src.main:create_app
# flask db upgrade

# ✅ Ejecutar tests antes de iniciar
echo "🧪 Ejecutando tests..."
pytest -v

# 🔥 Iniciar aplicación
echo "🔥 Iniciando aplicación..."
python src/main.py
