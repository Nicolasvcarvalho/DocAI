from fastapi.testclient import TestClient
from uuid import uuid4

from main import app

client = TestClient(app)

def test_criar_candidato():

    email = f"nicolas{uuid4()}@gmail.com"

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": email,
            "senha": "12345",
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 200

def test_login():

    response = client.post(
        "/login",
        json={"email": "nicolas@gmail.com", "senha": "12345"}
    )

    assert response.status_code == 200