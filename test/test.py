from fastapi.testclient import TestClient
from main import app   

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"full_name": "Johnathan Doe", "email": "johnathan.doe@xample.com", "nickname": "johnny", "password": "securePass123"})
    assert response.status_code == 201

def test_create_existing_user():
    response = client.post("/users/", json={"full_name": "Johnathan Doe", "email": "johnathan.doe@xample.com", "nickname": "johnny", "password": "securePass123"})
    assert response.status_code == 409