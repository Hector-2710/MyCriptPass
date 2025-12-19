import pytest

@pytest.mark.asyncio
async def test_create_user(ac):
    user = {
        "nickname": "usernumero1", 
        "email": "usernumero1@example.com", 
        "password": "securepassword", 
        "full_name": "Test User numero 1"
    }
    
    response = await ac.post("/users/", json=user)
    assert response.status_code == 201