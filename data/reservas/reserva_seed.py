# reservas_seed.py
from data.utils import enviar_post, get_token
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker("es_ES")

def poblar_reservas():
    headers = get_token()

    # 1. Crear áreas
    areas = []
    nombres_areas = ["Piscina", "Parrillera", "Salón de eventos", "Cancha"]
    for nombre in nombres_areas:
        data = {
            "name": nombre,
            "descripcion": f"Área {nombre.lower()} capacidad {random.randint(10,50)}",
            "deposit_amount": str(random.choice([0, 50, 80, 100])),  # algunas sin depósito
            "is_active": True,
        }
        res = enviar_post("/areas/", headers=headers, data=data)
        print("Área creada:", res)
        try:
            areas.append(res.get("id")) # type: ignore
        except Exception:
            pass

    # 2. Crear suministros para cada área
    for area_id in areas:
        for nombre in ["Sillas", "Mesas", "Parlantes"]:
            data = {
                "areacomun": area_id,
                "name": nombre,
                "descripcion": f"{nombre} de uso común",
                "cantidad_total": random.randint(5, 30)
            }
            res = enviar_post("/suministros/", headers=headers, data=data)
            print(f"Suministro {nombre} ->", res)

    # 3. Crear reservas
    reservas = []
    for i in range(20):  # 20 reservas de ejemplo
        unidad_id = random.randint(1, 50)
        area_id = random.choice(areas)
        start = datetime(2025, 10, random.randint(1, 20), 10, 0)
        end = start + timedelta(hours=3)
        data = {
            "unidad": unidad_id,
            "area": area_id,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "notas": fake.sentence(nb_words=5)
        }
        res = enviar_post("/reservas/", headers=headers, data=data)
        print("Reserva creada:", res)
        try:
            reservas.append(res)
        except Exception:
            pass

    # 4. Confirmar las reservas con depósito 0
    for r in reservas:
        try:
            reserva_id = r.get("id")
            # verificar si el área tiene depósito 0
            area_id = r.get("area")
            if not reserva_id or not area_id:
                continue
            # buscar el área creada
            # (si API no devuelve depósito, puedes usar el área en memoria)
            for a in areas:
                if a == area_id:
                    # confirmamos siempre, aquí asumo sin depósito
                    path = f"/reservas/{reserva_id}/confirmar/"
                    resp = enviar_post(path, headers=headers)
                    print(f"Reserva {reserva_id} confirmada ->", resp)
        except Exception as e:
            print("Error confirmando:", e)

if __name__ == "__main__":
    poblar_reservas()
