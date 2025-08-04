import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

load_dotenv()

Base = declarative_base()

ENV = os.getenv("ENV", "DEV")
if ENV == "TEST":
    SQLALCHEMY_DATABASE_URL = "sqlite://"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    USE_WINDOWS_AUTH = os.getenv("USE_WINDOWS_AUTH", "true").lower() == "true"
    DB_SERVER = os.getenv("DB_SERVER", "localhost")
    DB_NAME = os.getenv("DB_NAME", "VoleyTracker")

    if USE_WINDOWS_AUTH:
        # Autenticación con el usuario de Windows
        SQLALCHEMY_DATABASE_URL = (
            f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&trusted_connection=yes"
        )
    else:
        # Autenticación con usuario y contraseña
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        SQLALCHEMY_DATABASE_URL = (
            f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        )

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()