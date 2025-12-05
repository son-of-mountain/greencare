from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de la DB - Utilise /tmp sur Render (éphémère mais fonctionnel)
# Pour production, migrer vers PostgreSQL
db_path = os.getenv("DATABASE_PATH", "./data/greencare.db")
if os.getenv("RENDER"):
    # Sur Render, utiliser /tmp qui est accessible en écriture
    os.makedirs("/tmp/data", exist_ok=True)
    db_path = "/tmp/data/greencare.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# connect_args pour SQLite uniquement
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dépendance pour injecter la session DB dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
