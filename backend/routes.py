import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from backend.db import get_db
from backend.models import ActionDB, VoteDB, ActionCreate, VoteCreate, ActionResponse
router = APIRouter()

# --- CONFIGURATION PONDÉRATION (Règles Métier Numih) ---
ROLE_WEIGHTS = {
    "soignant": 1.5,   # Priorité au terrain
    "tech": 1.2,       # Expertise technique
    "cadre": 1.0,      # Standard
    "direction": 0.8,  # Moins de poids sur le "micro-opérationnel"
    "autre": 0.5
}

def compute_weighted_score(value: int, role: str) -> float:
    weight = ROLE_WEIGHTS.get(role.lower(), 0.5)
    return float(value * weight)

@router.post("/actions", response_model=ActionResponse)
def create_action(action: ActionCreate, db: Session = Depends(get_db)):
    # Initial score is 0
    db_action = ActionDB(**action.dict(), score=0.0)
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
        query = query.order_by(desc(ActionDB.id)) # Default: newest
        
    return query.all()


@router.post("/actions/{action_id}/vote")
def vote_action(action_id: int, vote: VoteCreate, db: Session = Depends(get_db)):
    # ... (Code de vote de l'étape 2 inchangé) ...
    # Assurez-vous d'avoir importé compute_weighted_score
    from backend.routes import compute_weighted_score # Ou redéfinir la fonction ici
    
    # (Copiez-collez la logique de vote de l'étape 2 ici pour être sûr)
    action = db.query(ActionDB).filter(ActionDB.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action non trouvée")
    
    existing_vote = db.query(VoteDB).filter(VoteDB.action_id == action_id, VoteDB.agent_id == vote.agent_id).first()
    weight_score = compute_weighted_score(vote.value, vote.role)

    if existing_vote:
        old_weight_score = compute_weighted_score(existing_vote.value, existing_vote.role)
        action.score -= old_weight_score
        existing_vote.value = vote.value
        existing_vote.role = vote.role
        action.score += weight_score
    else:
        new_vote = VoteDB(action_id=action_id, agent_id=vote.agent_id, value=vote.value, role=vote.role)
        db.add(new_vote)
        action.score += weight_score
    
    db.commit()
    return {"message": "A voté", "new_score": round(action.score, 2)}

# --- NOUVELLES ROUTES KPI ---

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    """Calcul des indicateurs d'impact global (somme des actions proposées)"""
    # Dans un vrai projet, on filtrerait sur les actions 'validées' par un comité.
    # Ici, pour le POC, on prend tout ce qui a un score positif > 0.
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
    """Export Open Data CSV des actions et leurs impacts"""
    actions = db.query(ActionDB).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    # Header CSV
    writer.writerow(['ID', 'Titre', 'Categorie', 'Service', 'Score', 'Gain_KWh', 'Gain_Euro', 'Gain_CO2'])
    
    for a in actions:
        writer.writerow([a.id, a.title, a.category, a.service_id, round(a.score, 2), a.gain_kwh, a.gain_euro, a.gain_co2])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=greencare_kpis.csv"}
    )
