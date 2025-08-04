import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

@pytest.fixture(scope="session")
def db_engine():
    # Crear motor SQLite en memoria
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    yield db
    
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    # Sobreescribir dependencia de la base de datos
    def override_get_db():
        yield db
        
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client