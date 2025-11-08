FROM python:3.11-slim

# Variables para evitar errores de Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ .

# Exponer puerto para FastAPI
EXPOSE 8000

# Por defecto, el comando lo define docker-compose
