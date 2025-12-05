# 🌱 GreenCare — Pilotage RSE Hospitalier "By Design"

> **Le module de pilotage RSE opérationnel pour l'écosystème Numih *dh*.**
> *Souverain, Éthique, Interopérable.*

![Badge HDS](https://img.shields.io/badge/Hébergement-HDS_Ready-blue)
![Badge Eco](https://img.shields.io/badge/Eco_Conception-A-green)
![Badge FHIR](https://img.shields.io/badge/Interop-HL7_FHIR-orange)

## 📋 Le Concept
Les établissements de santé peinent à concrétiser leur stratégie RSE sur le terrain. **GreenCare** est une brique logicielle transverse qui permet de :
1.  **Remonter** les initiatives terrain (Soignants, Techs, Admin).
2.  **Prioriser** démocratiquement les actions à fort impact.
3.  **Piloter** les gains réels (kWh, € , CO2) via des tableaux de bord décisionnels.

Conçu pour s'intégrer nativement au progiciel **dh**, GreenCare respecte les exigences de **Métamorph'OSE** : souveraineté des données, interopérabilité et sobriété numérique.

---

## 🚀 Démarrage Rapide

### Pré-requis
- Docker & Docker Compose
- Navigateur Web moderne (Pas d'internet requis)

### Installation & Lancement
```bash
# 1. Cloner le projet
git clone [https://github.com/votre-repo/greencare.git](https://github.com/votre-repo/greencare.git)
cd greencare

# 2. Lancer l'environnement (Build optimisé Multi-stage)
docker compose up --build -d

# 3. Accéder à l'application
# Frontend : http://localhost:8000/app/index.html
# API Docs : http://localhost:8000/docs

##🏗 Architecture & Choix Techniques
###Stack Sobriété "By Design"
Backend : Python FastAPI (Asynchrone, très faible empreinte mémoire).

Frontend : Vanilla JS + CSS (Aucun framework lourd type React/Angular à télécharger).

Database : SQLite (POC) / PostgreSQL (Prod).

Conteneur : Image Docker optimisée (< 150MB) basée sur python:3.10-slim.

###Sécurité & Souveraineté (HDS)
Données : Aucune donnée patient nominative stockée.

Headers : Politique CSP stricte, HSTS, X-Frame-Options (voir docs/souverainete_hds.md).

Infrastructure : Prêt pour déploiement sur Cloud Souverain Numih (SecNumCloud).

###Interopérabilité
Annuaire : Standard HL7 FHIR R4 (/fhir/Organization, /fhir/Practitioner).

Reporting : Exports Open Data (CSV/JSON) pour l'intégration décisionnelle.

## 📂 Structure du Projet
```
greencare/
├── backend/        # API FastAPI & Logique métier
├── frontend/       # Interface Utilisateur (Statique, léger)
├── data/           # Persistance (Volume Docker)
├── docker/         # Configuration conteneurisation
└── docs/           # Documentation technique & RSE
```
##📜 Licence
Projet Open Source - Licence MIT. Conçu pour le Challenge Numih France.
#### 2. Documentation d'Architecture
**Fichier :** `docs/architecture.md` (Nouveau)
Un schéma simple vaut 1000 mots pour un jury technique.

```markdown
# Architecture Technique GreenCare

## Vue d'ensemble
GreenCare est conçu comme un micro-service autonome pouvant être rattaché au SIH (Système d'Information Hospitalier) existant.

```mermaid
graph TD
    User[Utilisateur Hospitalier] -->|HTTPS / TLS 1.2| ReverseProxy[Reverse Proxy (Numih Cloud)]
    ReverseProxy -->|Port 8000| Container[Conteneur Docker GreenCare]
    
    subgraph "Conteneur Docker (HDS Ready)"
        API[FastAPI Backend]
        Static[Static Files Server]
        Middleware[Security Middleware]
        
        API -->|Lecture/Écriture| DB[(SQLite / Postgres)]
        API -->|Expose| FHIR[Endpoint FHIR]
        API -->|Expose| OpenData[Endpoint CSV/JSON]
    end
    
    API -.->|Intégration Future| ERP[ERP dh (Numih)]
```

##Flux de Données
Authentification : Délégable au SSO de l'hôpital (OpenID Connect) - Non implémenté dans le POC (Simulation par Rôle).

Saisie : Les données d'actions sont validées par Pydantic avant insertion.

Restitution :

Le Frontend consomme l'API REST JSON.

Les outils BI consomment l'API CSV.

L'annuaire consomme l'API FHIR.

#### 3. Le Script de Démo (Votre antisèche)
**Fichier :** `docs/demo_script.md` (Nouveau)
Suivez ce script à la lettre pendant votre présentation.

```markdown
# 🎤 Script de Démo - 3 Minutes Chrono

## 1. Introduction (30s)
* **Contexte :** "Bonjour. Aujourd'hui, l'hôpital produit des milliers de tonnes de déchets et consomme énormément d'énergie, mais les soignants n'ont aucun outil pour agir."
* **Solution :** "Voici GreenCare. Ce n'est pas une boîte à idées, c'est le module de pilotage RSE opérationnel connecté à l'écosystème Numih."

## 2. Démo Live (1m30s)
* **Action 1 (Dashboard) :** "Je suis Directeur. Je me connecte au Dashboard."
    * *Montrer `dashboard.html`.*
    * "En un coup d'œil, je vois mes gains réels : kWh, Euros, CO2. Ces données sont calculées en temps réel."
* **Action 2 (Interopérabilité) :** "Ces chiffres ne sont pas fermés. Je peux les exporter en un clic pour mon rapport annuel."
    * *Cliquer sur 'Export CSV' et ouvrir le fichier.*
* **Action 3 (Terrain) :** "Maintenant, je suis Infirmier de nuit au Bloc (Changer rôle menu déroulant)."
    * *Aller sur `index.html`.*
    * "Je vois les actions proposées. L'action 'Écrans Bloc Nuit' est pertinente. Je vote."
    * *Cliquer sur 'Pour'. Montrer le score qui change.*
    * "Mon vote a plus de poids car je suis soignant (+1.5)."

## 3. Technique & Conclusion (1m)
* **Architecture :** "Sous le capot, c'est du Numérique Responsable."
    * "Pas de framework lourd, mode sombre natif."
    * "Architecture Docker souveraine, prête pour vos datacenters HDS."
    * "Compatible FHIR pour l'annuaire."
* **Clôture :** "GreenCare est la brique manquante pour transformer les intentions RSE en résultats mesurables dans l'offre **dh**. Merci."

## Fichier : docs/qa_checklist.md (Nouveau) Pour être sûr de ne rien oublier avant de zipper.
