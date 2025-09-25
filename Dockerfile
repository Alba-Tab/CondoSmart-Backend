# Imagen base
FROM python:3.11-slim

# Evitar que Python guarde .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Generar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8080

# Comando de inicio
CMD ["gunicorn", "condoSmart.wsgi:application", "--bind", "0.0.0.0:8080"]
