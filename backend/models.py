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
    image_url = Column(String, nullable=True) # <-- NOUVEAU CHAMP IMAGE
    
    gain_kwh = Column(Float, default=0.0)
    gain_euro = Column(Float, default=0.0)
    gain_co2 = Column(Float, default=0.0)
    
    votes = relationship("VoteDB", back_populates="action")

class VoteDB(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    agent_id = Column(String)
    role = Column(String)
    value = Column(Integer)
    action = relationship("ActionDB", back_populates="votes")

class NewsDB(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String)  # "energie", "dechets", "innovation", "social"
    country = Column(String)  # Pays d'origine de l'actualité
    image_url = Column(String, nullable=True)
    source = Column(String, nullable=True)  # Source de l'info
    date = Column(String)  # Date de publication

# --- Pydantic Models ---
class ActionCreate(BaseModel):
    title: str
    description: str
    service_id: str
    category: str
    image_url: Optional[str] = None # <-- NOUVEAU DANS L'INPUT
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
    image_url: Optional[str] = None # <-- NOUVEAU DANS L'OUTPUT
    gain_kwh: float
    gain_euro: float
    gain_co2: float

    class Config:
        from_attributes = True

class NewsCreate(BaseModel):
    title: str
    description: str
    category: str
    country: str
    image_url: Optional[str] = None
    source: Optional[str] = None
    date: str

class NewsResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    country: str
    image_url: Optional[str] = None
    source: Optional[str] = None
    date: str

    class Config:
        from_attributes = True
