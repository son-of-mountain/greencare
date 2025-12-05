from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # <-- Ajout
from backend.db import engine, Base, SessionLocal
from backend.models import ActionDB
from backend.routes import router as api_router
from backend.fhir import router as fhir_router 

# Création des tables (Mode bourrin pour POC, en prod on utilise Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GreenCare API",
    description="API Module RSE - Numih",
    version="0.2.0"
)

# API Métier (Actions, Votes, KPIs)
app.include_router(api_router, prefix="/api", tags=["Métier RSE"])

# API Interopérabilité (FHIR)
# Numih : Standard FHIR pour les annuaires
app.include_router(fhir_router, prefix="/fhir", tags=["Interopérabilité FHIR"])

# --- SEED DATA (Données de test) ---

# Dans seed_data :
# ... imports ...
def seed_data():
    db = SessionLocal()
    if db.query(ActionDB).count() == 0:
        print("🌱 Seeding database with KPIs...")
        actions = [
            ActionDB(title="Écrans Bloc Nuit", description="Extinction auto.", service_id="BLOC", category="Energie", score=12.5, gain_kwh=5000, gain_euro=1200, gain_co2=400),
            ActionDB(title="Tri Déchets Box 1", description="Poubelles jaunes.", service_id="URG", category="Dechets", score=5.0, gain_kwh=0, gain_euro=3000, gain_co2=150),
            ActionDB(title="Covoit' Équipe Nuit", description="App dédiée.", service_id="RH", category="Social", score=2.0, gain_kwh=0, gain_euro=0, gain_co2=2000),
            ActionDB(title="Démat' Admission", description="Tablettes entrée.", service_id="ADM", category="Numerique", score=8.5, gain_kwh=100, gain_euro=500, gain_co2=50),
        ]
        db.add_all(actions)
        db.commit()
    db.close()

# Lancer le seed au démarrage
seed_data()

# montage des fichiers statiques(front)
# accessible via 8000 port
app.mount("/app",StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
async def root():
    return {
        "message": "GreenCare API is running", 
        "ui_url": "http://localhost:8000/app/"
    }
