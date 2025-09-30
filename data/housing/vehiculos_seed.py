import os
import sys
import random
import string # 1. Importa el módulo string

# --- Lógica para importar desde el directorio padre ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils import enviar_post, enviar_get, get_token
headers = get_token()
# 2. Función para generar placas con el formato específico
def generar_placa_aleatoria():
    """Genera una placa con formato NNNLLL o NNNNLLL."""
    # Decide aleatoriamente si la parte numérica tendrá 3 o 4 dígitos
    if random.choice([True, False]):
        numeros = str(random.randint(100, 999))
    else:
        numeros = str(random.randint(1000, 9999))
    
    # Genera 3 letras mayúsculas aleatorias
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    return f"{numeros}{letras}"

def poblar_vehiculos(n=100):
    print("Obteniendo lista de residentes...")
    try:
        # Obtenemos todas las residencias para asignar vehículos
        residencias_resp = enviar_get("/residencias/", headers=headers)
        if not residencias_resp or 'results' not in residencias_resp:
            print("Error: No se pudo obtener la lista de residencias.")
            return
        
        residencias = residencias_resp['results']
        if not residencias:
            print("No hay residencias para asignar vehículos. Abortando.")
            return
    except Exception as e:
        print(f"Ocurrió un error al obtener las residencias: {e}")
        return

    print(f"Creando {n} vehículos...")
    for i in range(n):
        # Elige una residencia al azar para asignarle el vehículo
        residencia_aleatoria = random.choice(residencias)
        
        data = {
            # 3. Usa la nueva función para generar la placa
            "placa": generar_placa_aleatoria(),
            "marca": random.choice(["Toyota", "Nissan", "Honda", "Suzuki", "Kia"]),
            "color": random.choice(["Rojo", "Blanco", "Negro", "Plata", "Azul"]),
            "observacion": "Vehículo de residente.",
            "unidad": residencia_aleatoria['unidad'],
            "responsable": residencia_aleatoria['user']
        }

        resp = enviar_post("/vehiculos/", headers=headers, data=data)
        if not resp is None:
            print(f"  Vehículo {i+1}/{n} creado: {resp.get('placa', 'Error')}")

if __name__ == "__main__":
    poblar_vehiculos(100)