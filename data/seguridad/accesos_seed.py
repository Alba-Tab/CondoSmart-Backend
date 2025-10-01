# accesos_seed.py
from data.utils import enviar_post, get_token
from faker import Faker
import os, random, time

fake = Faker("es_ES")
PHOTOS_DIR = "./visita_photos"

def crear_accesos_y_evidencias(n_accesos=50):
    headers = get_token()
    fotos = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith((".jpg",".png"))]
    if not fotos:
        raise SystemExit("No hay fotos en visita_photos/")

    for i in range(1, n_accesos+1):
        # Crear acceso
        data = {
            "unidad": random.randint(1, 50),
            "sentido": random.choice(["in", "out"]),
            "permitido": random.choice([True, False])
        }
        resp = enviar_post("/accesos/", headers=headers, data=data)
        print(f"[Acceso {i}] ->", resp)

        acceso_id = resp.get("id") if isinstance(resp, dict) else None
        if not acceso_id:
            continue  # si no devolvió ID, no se puede crear evidencia

        # Crear evidencia tipo "face"
        foto_path = os.path.join(PHOTOS_DIR, random.choice(fotos))
        edata = {
            "acceso": acceso_id,
            "modo": "face",
            "tipo": "externo"
        }
        with open(foto_path, "rb") as f:
            files = {"evidencia": f}
            eres = enviar_post("/accesos-evidencias/", headers=headers, data=edata, files=files)
        print(f"   -> evidencia face creada:", eres)

        time.sleep(0.05)  # un pequeño delay para no saturar

if __name__ == "__main__":
    crear_accesos_y_evidencias()
