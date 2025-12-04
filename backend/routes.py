from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.db import get_db
from backend.models import ActionDB, VoteDB, ActionCreate, VoteCreate, ActionResponse

router = APIRouter()

@router.post("/actions", response_model=ActionResponse)
def create_action(action: ActionCreate, db: Session = Depends(get_db)):
    db_action = ActionDB(**action.dict(), score=0)
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/actions", response_model=List[ActionResponse])
def read_actions(db: Session = Depends(get_db)):
    return db.query(ActionDB).all()

@router.post("/actions/{action_id}/vote")
def vote_action(action_id: int, vote: VoteCreate, db: Session = Depends(get_db)):
    action = db.query(ActionDB).filter(ActionDB.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action non trouvée")
    
    # Vérification vote existant (simplifié pour l'étape 1)
    existing_vote = db.query(VoteDB).filter(
        VoteDB.action_id == action_id, 
        VoteDB.agent_id == vote.agent_id
    ).first()

    if existing_vote:
        # On met à jour le vote existant
        # Note: La logique de recalcul du score global sera améliorée à l'étape 2
        diff = vote.value - existing_vote.value
        existing_vote.value = vote.value
        action.score += diff
    else:
        # Nouveau vote
        new_vote = VoteDB(action_id=action_id, agent_id=vote.agent_id, value=vote.value)
        db.add(new_vote)
        action.score += vote.value
    
    db.commit()
    return {"message": "A voté", "new_score": action.score}
