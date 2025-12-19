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


@pytest.mark.asyncio
async def test_create_user_fail_email(ac):
    user = {
        "nickname": "usernumero1", 
        "email": "usernumero1@example.com", 
        "password": "securepassword", 
        "full_name": "Test User numero 0"
    }

    user1 = {
        "nickname": "usernumero2", 
        "email": "usernumero1@example.com", 
        "password": "securepassword2", 
        "full_name": "Test User numero 1"
    }

    response = await ac.post("/users/", json=user)
    response1 = await ac.post("/users/", json=user1)
    
    assert response.status_code == 201
    assert response1.status_code == 409
    

@pytest.mark.asyncio
async def test_create_user_fail_nickname(ac):
    user = {
        "nickname": "usernumero1", 
        "email": "usernumero1@example.com", 
        "password": "securepassword", 
        "full_name": "Test User numero 0"
    }

    user2 = {
            "nickname": "usernumero1", 
            "email": "usernumero3@example.com", 
            "password": "securepassword2", 
            "full_name": "Test User numero 2"

        }
    
    response = await ac.post("/users/", json=user)
    response2 = await ac.post("/users/", json=user2)

    assert response.status_code == 201
    assert response2.status_code == 499

@pytest.mark.asyncio
async def test_create_user_fail_pydantic(ac):
    user = {
        "nickname": "us", 
        "email": "not-an-email", 
        "password": "pw", 
    }
    
    response = await ac.post("/users/", json=user)
    assert response.status_code == 422
