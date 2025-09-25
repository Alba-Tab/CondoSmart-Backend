#!/bin/sh
set -e

echo "Esperando DB..."
# espera hasta que la base de datos responda
until nc -z $DB_HOST $DB_PORT; do
  echo "DB aún no lista en $DB_HOST:$DB_PORT, reintentando..."
  sleep 2
done

echo "Aplicando migraciones..."
python3 manage.py migrate --noinput

echo "Iniciando Gunicorn..."
exec gunicorn condoSmart.wsgi:application --bind 0.0.0.0:8080