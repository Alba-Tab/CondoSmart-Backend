import sys
import os
import random
from faker import Faker

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.utils import enviar_post, enviar_get, get_token

fake = Faker("es_ES")

def poblar_residencias():
    headers = get_token()

    # 1. Obtiene todos los usuarios del grupo 'user' manejando paginación
    print("Obteniendo lista completa de usuarios del grupo 'user'...")
    all_user_ids = []
    url = "/users/?groups__name=user"
    
    try:
        while url:
            usuarios_resp = enviar_get(url, headers=headers)
            if not usuarios_resp or 'results' not in usuarios_resp:
                print("Error: No se pudo obtener la lista de usuarios o la respuesta no es válida.")
                print("Respuesta recibida:", usuarios_resp)
                return

            all_user_ids.extend([user['id'] for user in usuarios_resp['results']])
            
            next_url = usuarios_resp.get('next')
            if next_url:
                # La URL 'next' es absoluta, la convertimos en relativa para nuestra función
                url = next_url.split('/api/v1')[1]
            else:
                url = None
        
        print(f"Se encontraron {len(all_user_ids)} usuarios en total.")

        # 2. Selecciona aleatoriamente 150 usuarios de la lista total
        if len(all_user_ids) >= 150:
            user_ids = random.sample(all_user_ids, 150)
            print(f"Se han seleccionado aleatoriamente {len(user_ids)} usuarios para asignar residencias.")
        else:
            user_ids = all_user_ids
            print(f"Advertencia: Se encontraron menos de 150 usuarios. Se usarán los {len(user_ids)} disponibles.")

        if not user_ids:
            print("No hay usuarios disponibles para asignar. Abortando.")
            return

    except Exception as e:
        print(f"Ocurrió un error al obtener los usuarios: {e}")
        return

    # 3. Itera sobre las unidades y asigna los usuarios seleccionados
    for unidad_id in range(1, 51):
        if not user_ids:
            print("Se acabaron los usuarios para asignar. Terminando.")
            break

        # Asigna un propietario
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

        if not user_ids:
            print("No quedan más usuarios para asignar como residentes.")
            break
            
        # Decide si asignar residentes adicionales y cuántos
        num_residentes = random.randint(0, min(2, len(user_ids)))

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
