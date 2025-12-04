from fastapi import FastAPI
from backend.db import engine, Base, SessionLocal
from backend.models import ActionDB
from backend.routes import router

# Création des tables (Mode bourrin pour POC, en prod on utilise Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GreenCare API",
    description="API Module RSE - Numih",
    version="0.1.0"
)

app.include_router(router, prefix="/api")

# --- SEED DATA (Données de test) ---
# ... imports inchangés ...

# Dans seed_data :
def seed_data():
    db = SessionLocal()
    if db.query(ActionDB).count() == 0:
        print("🌱 Seeding database with Scoring V2...")
        actions = [
            ActionDB(title="Écrans Bloc Nuit", description="Extinction auto.", service_id="BLOC", category="Energie", score=12.5),
            ActionDB(title="Tri Déchets Box 1", description="Poubelles jaunes.", service_id="URG", category="Dechets", score=5.0),
            ActionDB(title="Covoit' Équipe Nuit", description="App dédiée.", service_id="RH", category="Social", score=2.0),
            ActionDB(title="Démat' Admission", description="Tablettes entrée.", service_id="ADM", category="Numerique", score=8.5),
        ]
        db.add_all(actions)
        db.commit()
        print("✅ Seed terminé.")
    db.close()

# ... le reste inchangé ...
# Lancer le seed au démarrage
seed_data()

@app.get("/")
async def root():
    return {"message": "GreenCare API is running", "status": "healthy"}
