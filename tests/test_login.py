import pytest
from app.auth.jwt import get_password_hash
from app.models.user import User
from app.models.role import Role

@pytest.fixture(scope="function", autouse=True)
def setup_test_user(db):
    # Crear rol admin
    admin_role = Role(id=1, name="admin")
    db.add(admin_role)
    db.commit()
    
    # Crear usuario de prueba
    test_user = User(
        email="testlogin@example.com",
        hashed_password=get_password_hash("testpassword"),
        role_id=1
    )
    db.add(test_user)
    db.commit()
    
    yield
    
    # Limpieza automática por el fixture de db

def test_login_success(client):
    response = client.post("/auth/login", json={
        "email": "testlogin@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_failure(client):
    response = client.post("/auth/login", json={
        "email": "noexist@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401