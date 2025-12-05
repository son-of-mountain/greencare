from fastapi.testclient import TestClient
from backend.main import app

# Client de test synchronisé (simule des requêtes HTTP)
client = TestClient(app)

def test_read_root():
    """Vérifie que l'API démarre et renvoie le statut healthy"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_security_headers():
    """Vérifie la conformité HDS (Headers de sécurité)"""
    response = client.get("/")
    # On vérifie que notre Middleware fait le job
    assert "strict-transport-security" in response.headers
    assert "content-security-policy" in response.headers
    assert response.headers["x-frame-options"] == "DENY"

def test_get_actions():
    """Vérifie qu'on récupère bien la liste des actions (Seed)"""
    response = client.get("/api/actions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4  # On doit avoir au moins les 4 actions du seed
    assert "score" in data[0]

def test_create_action_and_vote():
    """Scénario complet : Création -> Vote -> Vérif Score"""
    # 1. Création
    action_payload = {
        "title": "Test Auto",
        "description": "Test Pytest",
        "service_id": "TEST",
        "category": "Numerique"
    }
    res_create = client.post("/api/actions", json=action_payload)
    assert res_create.status_code == 200
    action_id = res_create.json()["id"]

    # 2. Vote (Rôle Direction = 0.8)
    vote_payload = {
        "agent_id": "TEST_BOT",
        "role": "direction",
        "value": 1
    }
    res_vote = client.post(f"/api/actions/{action_id}/vote", json=vote_payload)
    assert res_vote.status_code == 200
    
    # 3. Vérification du score pondéré
    # Le score initial est 0. Un vote direction vaut 0.8.
    assert res_vote.json()["new_score"] == 0.8

def test_fhir_endpoint():
    """Vérifie l'interopérabilité FHIR"""
    response = client.get("/fhir/Organization")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["resourceType"] == "Organization"
    assert "id" in data[0]
