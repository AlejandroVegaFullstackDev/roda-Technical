#!/bin/bash

echo "📋 Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

export PYTHONPATH=src

# ✅ Cargar variables del entorno desde .env si existe
if [ -f .env ]; then
  echo "📦 Cargando variables desde .env..."
  export $(grep -v '^#' .env | xargs)
fi

# ⏳ Esperar a que PostgreSQL esté disponible
echo "⏳ Esperando 10 segundos a que PostgreSQL inicie..."
sleep 10

export PGPASSWORD="$DB_PASSWORD"

# 🧪 Ejecutar tests antes de iniciar
echo "🧪 Ejecutando tests..."
pytest -v

# 🔥 Iniciar aplicación
echo "🔥 Iniciando aplicación..."
python src/main.py
