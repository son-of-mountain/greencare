from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
    service_id = Column(String)  # Ex: "BLOC", "RADIO"
    category = Column(String)    # Ex: "Energie", "Dechets", "Numerique"
    score = Column(Integer, default=0) # Score calculé
    
    votes = relationship("VoteDB", back_populates="action")

class VoteDB(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    agent_id = Column(String) # Identifiant agent (ex: matricule)
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
    value: int # 1 pour like, -1 pour dislike

class ActionResponse(BaseModel):
    id: int
    title: str
    description: str
    service_id: str
    category: str
    score: int

    class Config:
        from_attributes = True
