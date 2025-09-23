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
