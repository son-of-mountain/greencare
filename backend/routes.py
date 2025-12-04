from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
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
    action = db.query(ActionDB).filter(ActionDB.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action non trouvée")
    
    # Vérifier vote existant
    existing_vote = db.query(VoteDB).filter(
        VoteDB.action_id == action_id, 
        VoteDB.agent_id == vote.agent_id
    ).first()

    weight_score = compute_weighted_score(vote.value, vote.role)

    if existing_vote:
        # Annuler l'ancien score pondéré
        old_weight_score = compute_weighted_score(existing_vote.value, existing_vote.role)
        action.score -= old_weight_score
        
        # Mettre à jour le vote
        existing_vote.value = vote.value
        existing_vote.role = vote.role # Mise à jour du rôle possible
        
        # Ajouter nouveau score
        action.score += weight_score
    else:
        new_vote = VoteDB(
            action_id=action_id, 
            agent_id=vote.agent_id, 
            value=vote.value,
            role=vote.role
        )
        db.add(new_vote)
        action.score += weight_score
    
    db.commit()
    db.refresh(action)
    return {"message": "A voté", "new_score": round(action.score, 2)}
