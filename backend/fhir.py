from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# --- MODÈLES FHIR SIMPLIFIÉS (Pydantic) ---
# Numih utilise FHIR pour l'interopérabilité. 
# Ici on définit juste les champs essentiels pour le POC.

class FHIRMeta(BaseModel):
    versionId: str = "1"
    lastUpdated: str = "2025-01-01T12:00:00Z"

class FHIROrganization(BaseModel):
    resourceType: str = "Organization"
    id: str
    active: bool = True
    name: str
    alias: List[str] = []

class FHIRPractitioner(BaseModel):
    resourceType: str = "Practitioner"
    id: str
    active: bool = True
    name: list = [] # Family/Given structure simple
    gender: str = "unknown"

# --- DONNÉES SIMULÉES (MOCK) ---
# Dans la réalité, ces données viendraient de l'annuaire LDAP ou du SIH
# Pour le POC, on les code en dur pour montrer le format.

SERVICES_MOCK = [
    FHIROrganization(id="BLOC", name="Bloc Opératoire Central", alias=["BOC"]),
    FHIROrganization(id="URG", name="Service des Urgences", alias=["SAU"]),
    FHIROrganization(id="RADIO", name="Imagerie Médicale", alias=["RX"]),
    FHIROrganization(id="RH", name="Ressources Humaines"),
    FHIROrganization(id="ADM", name="Administration Générale"),
]

AGENTS_MOCK = [
    FHIRPractitioner(id="INFIRM01", name=[{"family": "Dubois", "given": ["Marie"]}], gender="female"),
    FHIRPractitioner(id="DOC01", name=[{"family": "Martin", "given": ["Jean"]}], gender="male"),
    FHIRPractitioner(id="DIR01", name=[{"family": "Bernard", "given": ["Sophie"]}], gender="female"),
]

# --- ENDPOINTS FHIR ---

@router.get("/Organization", response_model=List[FHIROrganization])
def get_organizations():
    """Retourne la liste des services au format FHIR"""
    return SERVICES_MOCK

@router.get("/Practitioner", response_model=List[FHIRPractitioner])
def get_practitioners():
    """Retourne la liste des agents (mock) au format FHIR"""
    return AGENTS_MOCK
