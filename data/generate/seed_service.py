import requests
import os

os.makedirs("dummy_photos", exist_ok=True)

def descargar_fotos(n=5):
    for i in range(n):
        url = "https://thispersondoesnotexist.com/"
        resp = requests.get(url, timeout=10)
        print(f"Descargando foto {i+1} de {n}...")
        if resp.status_code == 200:
            with open(f"dummy_photos/persona_{i}.jpg", "wb") as f:
                f.write(resp.content)
            print(f"Foto persona_{i}.jpg guardada")
        else:
            print("Error al descargar:", resp.status_code)

if __name__ == "__main__":
    descargar_fotos(200)
