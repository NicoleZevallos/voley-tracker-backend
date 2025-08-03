from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

Base = declarative_base()

# Detect test mode
IS_TEST = os.getenv("DB_TYPE", "real").lower() == "test"

if IS_TEST:
    # Use SQLite for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Use SQL Server for real environment
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    use_windows_auth = os.getenv("USE_WINDOWS_AUTH", "False").lower() == "true"

    if use_windows_auth:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes"
        )
    else:
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )

    params = urllib.parse.quote_plus(connection_string)
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Shared across both environments
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
