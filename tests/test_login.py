import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt import get_password_hash
from tests.test_db import engine, override_get_db, TestingSessionLocal
from app.models.user import User
from app.database import Base, get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_user():
    db = TestingSessionLocal()
    email = "testlogin@example.com"
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            new_user = User(
                email=email,
                hashed_password=get_password_hash("testpassword"),
                role_id=1
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        yield
        user_to_delete = db.query(User).filter(User.email == email).first()
        if user_to_delete:
            db.delete(user_to_delete)
            db.commit()
    finally:
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
