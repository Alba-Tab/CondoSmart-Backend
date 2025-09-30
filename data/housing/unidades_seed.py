from utils import enviar_post

def poblar_unidades():
    condominio_id = 1  # porque solo hay uno
    for piso in range(1, 11):          # 10 pisos
        for dpto in range(1, 6):       # 5 por piso
            code = f"{piso}{str(dpto).zfill(2)}"
            data = {
                "code": code,
                "is_active": True,
                "direccion": f"Piso {piso}, departamento {dpto}",
                "condominio": condominio_id,
                "piso": piso
            }
            resp = enviar_post("/unidades/", data=data)
            print("Unidad creada:", resp)

if __name__ == "__main__":
    poblar_unidades()
