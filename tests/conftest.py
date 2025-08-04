import pytest
from app.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    print("✅ Ejecutando fixture create_test_db")
    Base.metadata.create_all(bind=engine)
