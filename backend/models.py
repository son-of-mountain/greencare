from sqlalchemy import Column, Integer, String, Float, ForeignKey # Ajout Float
from sqlalchemy.orm import relationship
from backend.db import Base
from pydantic import BaseModel
from typing import Optional, List

# --- SQLAlchemy Models (Tables) ---
class ActionDB(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    service_id = Column(String)
    category = Column(String)
    score = Column(Float, default=0.0) # Changement en Float pour gérer les pondérations (ex: 1.2)
    
    votes = relationship("VoteDB", back_populates="action")

class VoteDB(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    agent_id = Column(String)
    role = Column(String)     # Nouveau : 'soignant', 'cadre', 'direction', 'autre'
    value = Column(Integer)   # +1 ou -1

    action = relationship("ActionDB", back_populates="votes")

# --- Pydantic Models (Validation API) ---
class ActionCreate(BaseModel):
    title: str
    description: str
    service_id: str
    category: str

class VoteCreate(BaseModel):
    agent_id: str
    role: str # Nouveau champ obligatoire
    value: int 

class ActionResponse(BaseModel):
    id: int
    title: str
    description: str
    service_id: str
    category: str
    score: float # Float ici aussi

    class Config:
        from_attributes = True
