import sys
import os
import random

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.utils import enviar_post, enviar_get, get_token

def poblar_pago_cargo():
    headers = get_token()

    # Obtener todos los pagos y cargos
    pagos_response = enviar_get("/pagos/", headers=headers)
    cargos_response = enviar_get("/cargos/", headers=headers)

    if not pagos_response or not 'results' in pagos_response:
        print("No se pudieron obtener los pagos. Abortando.")
        return

    if not cargos_response or not 'results' in cargos_response:
        print("No se pudieron obtener los cargos. Abortando.")
        return

    pagos_ids = [pago['id'] for pago in pagos_response['results']]
    cargos_ids = [cargo['id'] for cargo in cargos_response['results']]

    if not cargos_ids:
        print("No hay cargos disponibles para asociar. Abortando.")
        return

    # Crear una copia para poder eliminar los cargos ya usados
    cargos_disponibles = list(cargos_ids)

    for pago_id in pagos_ids:
        # Decidir cuántos cargos asociar a este pago (1, 2 o 3)
        num_cargos_a_asociar = random.randint(1, 3)
        
        # Asegurarse de no intentar tomar más cargos de los que quedan
        if num_cargos_a_asociar > len(cargos_disponibles):
            print(f"No quedan suficientes cargos para el pago {pago_id}. Se asociarán {len(cargos_disponibles)}.")
            num_cargos_a_asociar = len(cargos_disponibles)

        if num_cargos_a_asociar == 0:
            print("Se han asociado todos los cargos disponibles.")
            break

        # Seleccionar cargos aleatorios de la lista de disponibles
        cargos_seleccionados = random.sample(cargos_disponibles, num_cargos_a_asociar)

        for cargo_id in cargos_seleccionados:
            data = {
                "pago": pago_id,
                "cargo": cargo_id
            }
            resp = enviar_post("/pagocargo/", headers=headers, data=data)
            print(f"Asociando Cargo ID {cargo_id} a Pago ID {pago_id}: {resp}")
            
            # Eliminar el cargo usado de la lista de disponibles
            cargos_disponibles.remove(cargo_id)

if __name__ == "__main__":
    poblar_pago_cargo()
