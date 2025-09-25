# Imagen base oficial de Python 3.11
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema (necesarias para psycopg2 y netcat)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .
RUN mkdir -p /app/staticfiles

# Hacer ejecutable el entrypoint
RUN chmod +x entrypoint.sh

# Exponer puerto
EXPOSE 8080

# Usar entrypoint
ENTRYPOINT ["./entrypoint.sh"]
# Crear carpeta staticfiles
