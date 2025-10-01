from data.utils import enviar_post, get_token
from faker import Faker
import random
from datetime import date

fake = Faker("es_ES")

def poblar_pagos(n=30):
    headers = get_token()
    hoy = date.today()

    for _ in range(n):
        data = {
            "user": random.randint(1, 12),
            "fecha": str(hoy),
            "metodo": random.choice(["efectivo", "tarjeta", "transferencia"]),
            "estado": "pendiente",
            "referencia": fake.bothify(text="ref_##??")
        }
        resp = enviar_post("/pagos/", headers=headers, data=data)
        print("Pago creado:", resp)

if __name__ == "__main__":
    poblar_pagos()
