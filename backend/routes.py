import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from backend.db import get_db
from backend.models import ActionDB, VoteDB, ActionCreate, VoteCreate, ActionResponse, NewsDB, NewsCreate, NewsResponse

router = APIRouter()

# --- CONFIGURATION PONDÉRATION ---
ROLE_WEIGHTS = {
    "soignant": 1.5,
    "tech": 1.2,
    "cadre": 1.0,
    "direction": 0.8,
    "autre": 0.5
}

def compute_weighted_score(value: int, role: str) -> float:
    weight = ROLE_WEIGHTS.get(role.lower(), 0.5)
    return float(value * weight)

@router.post("/actions", response_model=ActionResponse)
def create_action(action: ActionCreate, db: Session = Depends(get_db)):
    # On utilise model_dump() pour Pydantic v2 au lieu de dict()
    action_data = action.model_dump() 
    
    # On force le score à 0.0 à la création
    db_action = ActionDB(**action_data, score=0.0)
    
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/actions", response_model=List[ActionResponse])
def read_actions(
    sort: Optional[str] = Query(None, regex="^(score|newest)$"), 
    db: Session = Depends(get_db)
):
    query = db.query(ActionDB)
    if sort == "score":
        query = query.order_by(desc(ActionDB.score))
    else:
        query = query.order_by(desc(ActionDB.id))
    return query.all()

@router.post("/actions/{action_id}/vote")
def vote_action(action_id: int, vote: VoteCreate, db: Session = Depends(get_db)):
    # 1. Vérifier si l'action existe
    action = db.query(ActionDB).filter(ActionDB.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action non trouvée")
    
    # 2. Vérifier vote existant
    existing_vote = db.query(VoteDB).filter(
        VoteDB.action_id == action_id, 
        VoteDB.agent_id == vote.agent_id
    ).first()

    # Calcul du poids du NOUVEAU vote
    weight_score = compute_weighted_score(vote.value, vote.role)

    if existing_vote:
        # Retirer l'ancien poids du score total
        old_weight_score = compute_weighted_score(existing_vote.value, existing_vote.role)
        action.score -= old_weight_score
        
        # Mettre à jour le vote
        existing_vote.value = vote.value
        existing_vote.role = vote.role
        
        # Ajouter le nouveau poids
        action.score += weight_score
    else:
        # Nouveau vote
        new_vote = VoteDB(
            action_id=action_id, 
            agent_id=vote.agent_id, 
            value=vote.value, 
            role=vote.role
        )
        db.add(new_vote)
        action.score += weight_score
    
    db.commit()
    return {"message": "A voté", "new_score": round(action.score, 2)}

# --- KPIS & EXPORTS ---

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    actions = db.query(ActionDB).filter(ActionDB.score > 0).all()
    
    total_kwh = sum(a.gain_kwh for a in actions)
    total_euro = sum(a.gain_euro for a in actions)
    total_co2 = sum(a.gain_co2 for a in actions)
    count = len(actions)

    return {
        "total_kwh": round(total_kwh, 2),
        "total_euro": round(total_euro, 2),
        "total_co2": round(total_co2, 2),
        "actions_count": count
    }

@router.get("/exports/kpis.csv")
def export_kpis_csv(db: Session = Depends(get_db)):
    actions = db.query(ActionDB).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Titre', 'Categorie', 'Service', 'Score', 'Gain_KWh', 'Gain_Euro', 'Gain_CO2'])
    
    for a in actions:
        writer.writerow([
            a.id, a.title, a.category, a.service_id, 
            round(a.score, 2), a.gain_kwh, a.gain_euro, a.gain_co2
        ])
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=greencare_kpis.csv"}
    )

# --- ACTUALITÉS RSE ---

@router.get("/news", response_model=List[NewsResponse])
def get_news(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(NewsDB)
    if category:
        query = query.filter(NewsDB.category == category)
    return query.order_by(desc(NewsDB.id)).all()

@router.post("/news", response_model=NewsResponse)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    db_news = NewsDB(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@router.post("/news/init")
def init_news_data(db: Session = Depends(get_db)):
    """Initialiser des actualités RSE génériques pour la démo"""
    
    # Vérifier si déjà initialisé
    if db.query(NewsDB).count() > 0:
        return {"message": "Données déjà initialisées"}
    
    sample_news = [
        {
            "title": "CHU de Lyon : -30% d'émissions CO2 grâce à l'optimisation énergétique",
            "description": "Le Centre Hospitalier Universitaire de Lyon a mis en place un système de gestion intelligente de l'énergie, permettant de réduire de 30% ses émissions de CO2. L'installation de capteurs IoT et l'optimisation des systèmes de chauffage ont généré une économie annuelle de 450 000€.",
            "category": "energie",
            "country": "France",
            "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800",
            "source": "Le Monde Santé",
            "date": "2024-11-15"
        },
        {
            "title": "Hopital de Singapour : 100% recyclage des déchets médicaux non-dangereux",
            "description": "Le Singapore General Hospital a atteint l'objectif ambitieux de recycler 100% de ses déchets médicaux non-dangereux. Grâce à un tri sélectif renforcé et des partenariats avec des entreprises de recyclage spécialisées, l'hôpital détourne 12 tonnes de déchets par jour des décharges.",
            "category": "dechets",
            "country": "Singapour",
            "image_url": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800",
            "source": "Healthcare Asia",
            "date": "2024-11-20"
        },
        {
            "title": "Hôpital de Copenhague : IA pour réduire le gaspillage alimentaire de 40%",
            "description": "Le Rigshospitalet de Copenhague utilise l'intelligence artificielle pour prédire précisément les besoins alimentaires des patients. Cette innovation a permis de réduire le gaspillage alimentaire de 40%, soit 80 tonnes par an, tout en améliorant la satisfaction des patients.",
            "category": "innovation",
            "country": "Danemark",
            "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800",
            "source": "Nordic Healthcare Journal",
            "date": "2024-11-10"
        },
        {
            "title": "NHS UK : Programme mobilité douce pour 15 000 soignants",
            "description": "Le National Health Service britannique lance un programme ambitieux de mobilité douce : vélos électriques, transports en commun gratuits et covoiturage pour 15 000 soignants. Objectif : réduire de 25% l'empreinte carbone des déplacements domicile-travail d'ici 2025.",
            "category": "social",
            "country": "Royaume-Uni",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
            "source": "The Guardian Health",
            "date": "2024-11-25"
        },
        {
            "title": "Hôpital de Tokyo : panneaux solaires produisent 60% de l'électricité",
            "description": "L'Hôpital universitaire de Tokyo a installé 5 000 m² de panneaux solaires sur ses toits et parkings. La production couvre désormais 60% des besoins électriques de l'établissement, évitant l'émission de 800 tonnes de CO2 par an.",
            "category": "energie",
            "country": "Japon",
            "image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800",
            "source": "Tokyo Medical News",
            "date": "2024-11-05"
        },
        {
            "title": "Clinique de Montréal : premier hôpital carboneutre d'Amérique du Nord",
            "description": "Le Centre Hospitalier de l'Université de Montréal (CHUM) devient le premier hôpital carboneutre d'Amérique du Nord. Grâce à la géothermie, l'efficacité énergétique et la compensation carbone, l'établissement atteint la neutralité carbone avec 3 ans d'avance.",
            "category": "innovation",
            "country": "Canada",
            "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800",
            "source": "Radio Canada",
            "date": "2024-12-01"
        },
        {
            "title": "Hôpital de Berlin : programme bien-être réduit le burn-out de 35%",
            "description": "La Charité de Berlin a lancé un programme holistique de bien-être pour son personnel soignant : espaces de repos, téléconsultations psychologiques, horaires flexibles. Résultat : une baisse de 35% des cas de burn-out et une amélioration notable de la qualité des soins.",
            "category": "social",
            "country": "Allemagne",
            "image_url": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=800",
            "source": "Deutsche Welle Health",
            "date": "2024-11-18"
        },
        {
            "title": "Barcelone : circuit court pour l'alimentation hospitalière bio",
            "description": "Les hôpitaux de Barcelone s'approvisionnent désormais à 70% auprès de producteurs locaux bio dans un rayon de 50km. Cette initiative soutient l'économie locale, réduit les émissions de transport et améliore la qualité nutritionnelle des repas.",
            "category": "dechets",
            "country": "Espagne",
            "image_url": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=800",
            "source": "El País Salud",
            "date": "2024-11-22"
        }
    ]
    
    for news_data in sample_news:
        db_news = NewsDB(**news_data)
        db.add(db_news)
    
    db.commit()
    return {"message": f"{len(sample_news)} actualités initialisées avec succès"}
