from utils import enviar_post, get_token

HEADERS = get_token()

def crear_condominio():
    data = {
        "direccion": "Av. Principal 123",
        "name": "Condominio Central",
        "tipo": "vertical"
    }
    resp = enviar_post("/condominios/", headers=HEADERS, data=data)
    print("Condominio creado:", resp)

if __name__ == "__main__":
    crear_condominio()