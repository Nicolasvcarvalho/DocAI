from fastapi.testclient import TestClient
from uuid import uuid4

from main import app

client = TestClient(app)

def test_criar_candidato_e_logar_candidato():

    email = f"nicolas{uuid4()}@gmail.com"
    senha = "123"

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": email,
            "senha": senha,
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 200

    
    response = client.post(
        "/login",
        json={"email": email, "senha": senha}
    )

    assert response.status_code == 200

def test_email_duplicado():

    email = f"nicolas{uuid4()}@gmail.com"
    senha = "123"

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": email,
            "senha": senha,
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 200

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": email,
            "senha": senha,
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 400
    assert response.json()['detail'] == "Email já cadastrado"

def test_senha_errada():

    email = f"nicolas{uuid4()}@gmail.com"
    senha = "123"

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": email,
            "senha": senha,
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 200
    
    response = client.post(
        "/login",
        json={"email": email, "senha": "senha_errada"}
    )

    assert response.status_code == 401
    assert response.json()['detail'] == "Email ou senha inválidos"