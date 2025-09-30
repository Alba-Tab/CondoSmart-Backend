import requests
from faker import Faker

# Inicializamos generador de datos
fake = Faker('es_ES')

# Endpoint base de tu API
API_BASE = "http://localhost:8000/api"
# Token si tu API usa autenticación
AUTH_HEADERS = {
    "Authorization": "Bearer TU_TOKEN_AQUI"
}

def poblar_usuarios(n=10):
    for _ in range(n):
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": "Test1234!",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        # Si tu endpoint también recibe archivo (ej: foto de perfil a S3)
        files = {"photo": open("dummy.jpg", "rb")}  # puedes generar imágenes dummy
        resp = requests.post(f"{API_BASE}/users/", data=data, files=files, headers=AUTH_HEADERS)
        
        if resp.status_code == 201:
            print("Usuario creado:", resp.json())
        else:
            print("Error:", resp.status_code, resp.text)

def poblar_condominios(n=5):
    for _ in range(n):
        data = {
            "name": fake.company(),
            "direccion": fake.address(),
            "tipo": "horizontal"  # o "vertical"
        }
        resp = requests.post(f"{API_BASE}/condominios/", json=data, headers=AUTH_HEADERS)
        if resp.status_code == 201:
            print("Condominio creado:", resp.json())
        else:
            print("Error:", resp.status_code, resp.text)

if __name__ == "__main__":
    poblar_condominios(3)
    poblar_usuarios(5)