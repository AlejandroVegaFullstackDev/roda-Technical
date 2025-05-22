# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Permitir ejecución del script
RUN chmod +x run.sh

# Puerto que expone Flask
EXPOSE 5000

# Comando para ejecutar al iniciar el contenedor
CMD ["./run.sh"]
