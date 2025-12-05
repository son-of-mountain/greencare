import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from backend.db import get_db
from backend.models import ActionDB, VoteDB, ActionCreate, VoteCreate, ActionResponse

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
