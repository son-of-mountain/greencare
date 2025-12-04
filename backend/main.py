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
def seed_data():
    db = SessionLocal()
    if db.query(ActionDB).count() == 0:
        print("🌱 Seeding database...")
        actions = [
            ActionDB(title="Écrans Bloc Opératoire", description="Extinction auto des écrans du bloc de 22h à 6h.", service_id="BLOC", category="Energie", score=10),
            ActionDB(title="Tri DASRI Urgences", description="Formation flash et nouvelles poubelles jaunes aux box 1-4.", service_id="URG", category="Dechets", score=5),
            ActionDB(title="Covoit' Nuit", description="Application covoiturage pour l'équipe de nuit.", service_id="RH", category="Social", score=2),
            ActionDB(title="Zéro Papier Admission", description="Numérisation complète du dossier d'entrée.", service_id="ADM", category="Numerique", score=8),
        ]
        db.add_all(actions)
        db.commit()
        print("✅ Seed terminé.")
    db.close()

# Lancer le seed au démarrage
seed_data()

@app.get("/")
async def root():
    return {"message": "GreenCare API is running", "status": "healthy"}
