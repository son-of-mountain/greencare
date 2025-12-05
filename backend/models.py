from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.db import Base
from pydantic import BaseModel
from typing import Optional, List

# --- SQLAlchemy Models ---
class ActionDB(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    service_id = Column(String)
    category = Column(String)
    score = Column(Float, default=0.0)
    
    # Nouveaux champs d'impact (Sobriété & Économies)
    gain_kwh = Column(Float, default=0.0)  # Énergie économisée
    gain_euro = Column(Float, default=0.0) # Économies financières
    gain_co2 = Column(Float, default=0.0)  # Kg CO2 évités
    
    votes = relationship("VoteDB", back_populates="action")

class VoteDB(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    agent_id = Column(String)
    role = Column(String)
    value = Column(Integer)
    action = relationship("ActionDB", back_populates="votes")

# --- Pydantic Models ---
class ActionCreate(BaseModel):
    title: str
    description: str
    service_id: str
    category: str
    # Champs optionnels lors de la création
    gain_kwh: Optional[float] = 0.0
    gain_euro: Optional[float] = 0.0
    gain_co2: Optional[float] = 0.0

class VoteCreate(BaseModel):
    agent_id: str
    role: str
    value: int 

class ActionResponse(BaseModel):
    id: int
    title: str
    description: str
    service_id: str
    category: str
    score: float
    gain_kwh: float
    gain_euro: float
    gain_co2: float

    class Config:
        from_attributes = True
