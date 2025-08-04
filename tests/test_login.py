import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt import get_password_hash
from tests.test_db import override_get_db
from app.models.user import User
from app.models.role import Role
from app.database import get_db, SessionLocal

# Sobreescribir dependencia para usar base de datos de prueba
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_user():
    db = SessionLocal()
    email = "testlogin@example.com"

    # Crear rol admin si no existe
    if not db.query(Role).filter(Role.id == 1).first():
        admin_role = Role(id=1, name="admin")
        db.add(admin_role)
        db.commit()

    # Crear usuario de prueba si no existe
    if not db.query(User).filter(User.email == email).first():
        new_user = User(
            email=email,
            hashed_password=get_password_hash("testpassword"),
            role_id=1
        )
        db.add(new_user)
        db.commit()

    yield

    # Limpieza después de las pruebas
    if user := db.query(User).filter(User.email == email).first():
        db.delete(user)
        db.commit()
    db.close()

def test_login_success():
    response = client.post("/auth/login", json={
        "email": "testlogin@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    response = client.post("/auth/login", json={
        "email": "noexist@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"