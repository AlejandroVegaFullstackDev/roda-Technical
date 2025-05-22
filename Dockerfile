# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Dar permisos al script
RUN chmod +x run.sh

# Exponer puerto Flask
EXPOSE 5000

# Comando por defecto
CMD ["./run.sh"]
