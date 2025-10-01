# visitas_seed.py
from data.utils import enviar_post, get_token
from faker import Faker
import os, random

fake = Faker("es_ES")
PHOTOS_DIR = "./visita_photos"

def poblar_visitas(n=50):
    headers = get_token()
    fotos = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith((".jpg",".png"))]
    if not fotos:
        raise SystemExit("No hay fotos en visits_photos/")
    for i in range(n):
        foto_path = os.path.join(PHOTOS_DIR, random.choice(fotos))
        data = {
            "name": fake.name(),
            "documento": fake.bothify(text="########"),
            "telefono": fake.msisdn()[:9],
            "is_active": "true"
        }
        with open(foto_path, "rb") as f:
            files = {"photo": f}
            resp = enviar_post("/visitas/", headers=headers, data=data, files=files)
        print(f"[Visita {i+1}] ->", resp)

if __name__ == "__main__":
    poblar_visitas(50)
