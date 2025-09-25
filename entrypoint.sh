#!/bin/sh
set -e

echo "▶️ Aplicando migraciones..."
python3 manage.py migrate --noinput

echo "▶️ Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput

echo "▶️ Iniciando Gunicorn..."
exec gunicorn condoSmart.wsgi:application --bind 0.0.0.0:8080
