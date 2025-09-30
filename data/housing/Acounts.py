import os
import random
from faker import Faker
from utils import enviar_post

fake = Faker("es_ES")

# --- Hacemos la ruta más robusta ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'dummy_photos')

def poblar_usuarios(n=5):
    # Obtenemos la lista de fotos disponibles
    try:
        fotos = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg", ".png"))]
    except FileNotFoundError:
        fotos = [] # Si el directorio no existe, la lista de fotos está vacía

    for i in range(n):
        print(f"Creando usuario {i+1}/{n}...")
        data = {
            "username": fake.unique.user_name(),
            "password": "Test1234!",
            "ci": str(fake.unique.random_int(1000000, 9999999)),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "is_active": "True",
            "groups": random.choice(["admin", "user", "guard","user","user","user"]),
        }

        files = None
        img_path = None
        
        if fotos:
            # 2. Elige una foto al azar y la elimina de la lista para no repetirla
            foto_elegida = fotos.pop(random.randrange(len(fotos)))
            img_path = os.path.join(IMAGES_DIR, foto_elegida)
            
            with open(img_path, "rb") as f:
                files = {"photo": (foto_elegida, f.read())}
                resp = enviar_post("/users/", data=data, files=files)
                print("  Creado con foto:", resp)
            try:
                os.remove(img_path)
                print(f"  Foto {foto_elegida} eliminada.")
            except OSError as e:
                print(f"  Error al eliminar la foto: {e}")
        else:
            print("  No hay más fotos disponibles. Creando usuario sin foto.")
            resp = enviar_post("/users/", data=data)
            print("  Creado sin foto:", resp)


if __name__ == "__main__":
    poblar_usuarios(500) 