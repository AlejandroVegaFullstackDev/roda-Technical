#!/bin/bash

echo "📋 Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# 🧪 Crear .env si no existe
if [ ! -f .env ]; then
  echo "🆕 Creando archivo .env predeterminado..."
  cat <<EOF > .env
DB_USER=postgres
DB_PASSWORD=roda724
DB_NAME=roda_db
DB_HOST=localhost
DB_PORT=5432

JWT_SECRET_KEY=supersecretjwtkey
JWT_ACCESS_TOKEN_EXPIRES=3600

FLASK_ENV=development
EOF
fi

echo "🚀 Exportando variables de entorno..."
export PYTHONPATH=src
export $(grep -v '^#' .env | xargs)

echo "🔥 Iniciando aplicación..."
python src/main.py
