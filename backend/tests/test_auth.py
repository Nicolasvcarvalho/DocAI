from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_criar_candidato():

    response = client.post(
        "/candidatos",
        json={
            "nome": "Nicolas",
            "sobrenome": "Carvalho",
            "sexo": "MASCULINO",
            "email": "nicolas@gmail.com",
            "senha": "12345",
            "data_nascimento": "2025-10-22"
        }
    )

    assert response.status_code == 200
