from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

# Base de datos SQLite en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Sesión de prueba
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas antes de usar
Base.metadata.create_all(bind=engine)

# Dependency override para pruebas
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
