from data.utils import enviar_post, get_token
from faker import Faker
import random

fake = Faker("es_ES")

def poblar_mascotas():
    headers = get_token()
    for _ in range(50):
        data = {
            "responsable": random.randint(1, 500),
            "name": fake.first_name(),
            "tipo": random.choice(["perro", "gato"]),
            "raza": random.choice(["Labrador", "Bulldog", "Siames", "Persa"]),
            "activo": True,
            "desde": "2025-02-01"
        }
        resp = enviar_post("/mascotas/", headers=headers, data=data)
        print("Mascota creada:", resp)

if __name__ == "__main__":
    poblar_mascotas()
