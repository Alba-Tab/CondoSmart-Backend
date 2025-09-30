from utils import enviar_post, enviar_get, get_token
from faker import Faker
import random

fake = Faker("es_ES")

def poblar_residencias():
    # 2. Obtiene todos los usuarios que pertenecen al grupo "user"
    print("Obteniendo lista de usuarios del grupo 'user'...")
    try:
        # Asumimos que tu API de usuarios permite filtrar por grupo
        headers = get_token()
        usuarios_resp = enviar_get("/users/?groups__name=user", headers=headers)
        if not usuarios_resp or 'results' not in usuarios_resp:
            print("Error: No se pudo obtener la lista de usuarios o la respuesta no es válida.")
            print("Respuesta recibida:", usuarios_resp)
            return
        
        # Extraemos solo los IDs de los usuarios
        user_ids = [user['id'] for user in usuarios_resp['results']]
        
        if not user_ids:
            print("No se encontraron usuarios en el grupo 'user'. Abortando.")
            return
            
        print(f"Se encontraron {len(user_ids)} usuarios.")

    except Exception as e:
        print(f"Ocurrió un error al obtener los usuarios: {e}")
        return

    # 3. Itera sobre las unidades y asigna los usuarios
    for unidad_id in range(1, 51):
        # Asegúrate de no intentar asignar más residentes que usuarios disponibles
        if not user_ids:
            print("Se acabaron los usuarios para asignar. Terminando.")
            break

        # Asigna un propietario y varios residentes
        max_posibles = len(user_ids) - 1
        if max_posibles <= 0:
            num_residentes = 0
        else:
            num_residentes = random.randint(1, min(3, max_posibles))
        
        # Asigna el propietario
        if user_ids:
            owner_id = user_ids.pop(random.randrange(len(user_ids)))
            data_owner = {
                "user": owner_id,
                "unidad": unidad_id,
                "is_owner": True,
                "tipo_ocupacion": "propietario",
                "status": "activa",
                "start": "2025-01-01"
            }
            resp = enviar_post("/residencias/", headers=headers, data=data_owner)
            print(f"  Propietario {owner_id} asignado a unidad {unidad_id}: {resp}")

        # Asigna los otros residentes
        for _ in range(num_residentes):
            if not user_ids:
                break
            
            residente_id = user_ids.pop(random.randrange(len(user_ids)))
            data_residente = {
                "user": residente_id,
                "unidad": unidad_id,
                "is_owner": False,
                "tipo_ocupacion": "residente",
                "status": "activa",
                "start": "2025-01-01"
            }
            resp = enviar_post("/residencias/", headers=headers, data=data_residente)
            print(f"  Residente {residente_id} asignado a unidad {unidad_id}: {resp}")

if __name__ == "__main__":
    poblar_residencias()
