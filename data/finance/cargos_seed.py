from data.utils import enviar_post, get_token
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker("es_ES")

def poblar_cargos(n=50):
    headers = get_token()
    hoy = date.today()

    for unidad_id in range(1, 51):  # 50 unidades
        monto = random.choice([50, 80, 100, 120])
        periodo = hoy + timedelta(days=random.randint(10, 90))

        data = {
            "unidad": unidad_id,
            "concepto": "multa",
            "descripcion": fake.sentence(),
            "monto": monto,
            "periodo": str(periodo),
            "estado": "pendiente",
            "saldo": monto
        }
        resp = enviar_post("/cargos/", headers=headers, data=data)
        print("Cargo creado:", resp)

if __name__ == "__main__":
    poblar_cargos()
