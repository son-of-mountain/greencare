from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.db import engine, Base, SessionLocal
from backend.models import ActionDB
from backend.routes import router as api_router
from backend.fhir import router as fhir_router
from backend.security import SecurityHeadersMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GreenCare API", version="0.5.0")

# Sécurité HDS
app.add_middleware(SecurityHeadersMiddleware)

# Routes
app.include_router(api_router, prefix="/api", tags=["Métier RSE"])
app.include_router(fhir_router, prefix="/fhir", tags=["Interopérabilité FHIR"])

app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

# Redirection de la racine vers la page d'accueil
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/app/landing.html")

# --- SEED DATA AVEC IMAGES ---
def seed_data():
    db = SessionLocal()
    if db.query(ActionDB).count() == 0:
        print("🌱 Seeding database with Visuals...")
        actions = [
            ActionDB(
                title="Écrans Bloc Nuit", 
                description="Extinction automatique des moniteurs du bloc opératoire de 22h à 6h pour réduire la consommation.", 
                service_id="BLOC", 
                category="Energie", 
                score=18.5, 
                gain_kwh=5000, gain_euro=1200, gain_co2=400,
                image_url="https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=800&q=80" # Salle d'opération
            ),
            ActionDB(
                title="Tri Déchets Box 1", 
                description="Installation de poubelles jaunes dédiées aux emballages stériles dans les box d'urgence.", 
                service_id="URG", 
                category="Dechets", 
                score=12.0, 
                gain_kwh=0, gain_euro=3000, gain_co2=150,
                image_url="https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&w=800&q=80" # Tri médical
            ),
            ActionDB(
                title="Démat' Admission", 
                description="Utilisation de tablettes pour l'admission patient, supprimant 15000 feuilles/an.", 
                service_id="ADM", 
                category="Numerique", 
                score=8.5, 
                gain_kwh=100, gain_euro=500, gain_co2=50,
                image_url="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80" # Tablette médicale
            ),
             ActionDB(
                title="Mobilité Douce", 
                description="Création d'un parking vélo sécurisé pour inciter le personnel à venir sans voiture.", 
                service_id="RH", 
                category="Transport", 
                score=6.0, 
                gain_kwh=0, gain_euro=0, gain_co2=2500,
                image_url="https://images.unsplash.com/photo-1571333250630-f0230c320b6d?auto=format&fit=crop&w=800&q=80" # Vélo
            ),
        ]
        db.add_all(actions)
        db.commit()
    db.close()

seed_data()

# Plus de route /root redondante car elle est définie plus haut
