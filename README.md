# Guia de instalacion

## Empecemos por lo basico en shell

No olvidar tener creado la base en posggreSQL

```Shell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Credenciales ya creadas

Esto es lo generado con create superuser

```Shell
Username: albaro
Email address: albaro@gmail.com
Password:
Password (again):
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## ahora en postman

Para empezar tenemos que hacer un login y poner el token valido en access para asi poder acceder a nuestros demas metodos que necsitan un login necesariamente.

## yml si uso base de datos con contenedores

```Shell
version: "3.9"

services:
web:
  build: .
  container_name: django_app
  volumes:
    - .:/app
  ports:
    - "8000:8000"
  depends_on:
    - db
  environment:
    - DJANGO_SETTINGS_MODULE=condoSmart.settings
    - POSTGRES_DB=${DB_NAME}
    - POSTGRES_USER=${DB_USER}
    - POSTGRES_PASSWORD=${DB_PASSWORD}
    - POSTGRES_HOST=db

db:
  image: postgres:16
  container_name: postgres_db
  restart: always
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"

pgadmin:
  image: dpage/pgadmin4:8
  container_name: pgadmin4
  restart: always
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@admin.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  depends_on:
    - db
  volumes:
    - pgadmin_data:/var/lib/pgadmin

volumes:
  postgres_data:
  pgadmin_data:

```
