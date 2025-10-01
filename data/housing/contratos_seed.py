from data.utils import enviar_post, get_token
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker("es_ES")

def poblar_contratos():
    headers = get_token()
    for unidad_id in range(1, 51):  # 50 unidades
        start = fake.date_this_year()
        end = (date.fromisoformat(str(start)) + timedelta(days=365 * random.choice([1, 2]))).isoformat()
        
        data = {
            "unidad": unidad_id,
            "inquilino": random.randint(1, 500),
            "monto_mensual": 350.00,
            "start": str(start),
            "end": end,
            "duenno": random.randint(1, 500),
            "descripcion": fake.sentence(),
        }
        resp = enviar_post("/contratos/", headers=headers, data=data)
        
        print("Contrato creado:", resp)

if __name__ == "__main__":
    poblar_contratos()
