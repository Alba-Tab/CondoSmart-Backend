import runpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def run_seed(path):
    full_path = os.path.join(DATA_DIR, path)
    print(f"==> Ejecutando {path}")
    runpy.run_path(full_path, run_name="__main__")

if __name__ == "__main__":
    # 1. Seguridad / Accounts
    run_seed("Acounts.py")

    # 2. Housing
    run_seed("housing/condominio_seed.py")
    run_seed("housing/unidades_seed.py")
    run_seed("housing/residencias_seed.py")
    run_seed("housing/mascotas_seed.py")
    run_seed("housing/vehiculos_seed.py")

    # 3. Finance
    run_seed("finance/cargos_seed.py")
    run_seed("finance/pagos_seed.py")
    run_seed("finance/pago_cargo_seed.py")

    # 4. Reservas
    run_seed("reservas/reserva_seed.py")

    # 5. Seguridad
    run_seed("seguridad/visitas_seed.py")
    run_seed("seguridad/accesos_seed.py")
