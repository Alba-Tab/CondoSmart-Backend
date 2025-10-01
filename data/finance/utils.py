import requests
from faker import Faker
import random
import os

fake = Faker("es_ES")

API_BASE = "http://localhost:8000/api/v1"
USERNAME = "albaro"
PASSWORD = "1234"

def get_token():
    """Autenticarse y devolver headers con Bearer token"""
    resp = requests.post(
        f"{API_BASE}/token/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    if resp.status_code == 200:
        token = resp.json()["access"]
        return {"Authorization": f"Bearer {token}"}
    else:
        raise Exception(f"Error al obtener token: {resp.status_code} {resp.text}")

def enviar_post(path, headers, data=None, files=None):
    resp = requests.post(f"{API_BASE}{path}", data=data, files=files, json=data if files is None else None, headers=headers)
    if resp.status_code in (200, 201):
        return resp.json()
    else:
        print(f"Error {resp.status_code} → {resp.text}")
        return None

def enviar_get(path, headers, params=None):
    resp = requests.get(f"{API_BASE}{path}", params=params, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Error {resp.status_code} → {resp.text}")
        return None
    
