# incidentes_seed.py
from utils import enviar_post, get_token
from faker import Faker
import os, random
from datetime import date, timedelta
import sys

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Directorio de fotos de dummy
PHOTOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dummy_photos')

fake = Faker("es_ES")

def poblar_incidentes(n_incidentes=10):
    headers = get_token()
    fotos = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith((".jpg",".png"))]
    if not fotos:
        fotos = []

    for i in range(n_incidentes):
        unidad = random.randint(1, 50)
        user = random.randint(1, 12)  # Asumiendo que hay 120 usuarios
        titulo = fake.sentence(nb_words=3).rstrip('.')
        descripcion = fake.text(max_nb_chars=120)
        monto_multa = random.choice([50, 80, 120, 200])

        data = {
            "unidad": unidad,
            "user": user,
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": "abierto",
            "monto_multa": monto_multa
        }

        # Siempre enviar sin evidencia
        resp = enviar_post("/incidentes/", headers=headers, data=data)

        print(f"[Incidente {i+1}] ->", resp)
        # generar cargo para el incidente si endpoint existe /incidentes/{id}/generar_cargo/
        try:
            incidente_id = resp.get("id")#type: ignore
        except Exception:
            incidente_id = None

        if incidente_id:
            cargo_data = {"monto_multa": float(monto_multa)}
            resp_cargo = enviar_post(f"/incidentes/{incidente_id}/generar_cargo/", headers=headers, data=cargo_data)
            print("  -> cargo generado:", resp_cargo)

if __name__ == "__main__":
    poblar_incidentes(10)
