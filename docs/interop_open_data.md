# Stratégie d'Interopérabilité & Open Data

Conformément à la stratégie **Numih "Métamorph'OSE"** et au cadre d'urbanisation des SI de santé (CI-SIS), GreenCare adopte une approche standardisée pour ses échanges de données.

## 1. Annuaire & Structure : Standard HL7 FHIR
Nous utilisons le standard **FHIR R4** (Fast Healthcare Interoperability Resources) pour référencer les acteurs et structures. Cela garantit que GreenCare peut s'interfacer nativement avec :
- Le progiciel **dh** (Gestion administrative).
- Les annuaires nationaux (RPPS).

**Endpoints implémentés :**
- `GET /fhir/Organization` : Liste des services hospitaliers (Bloc, Urgences...).
- `GET /fhir/Practitioner` : Liste des professionnels (Agents, Médecins...).

## 2. Indicateurs RSE : Open Data (CSV/JSON)
Pour les données d'impact (consommation, déchets), nous privilégions des formats ouverts et simples (**CSV**, **JSON**) pour faciliter :
- L'intégration dans des outils décisionnels (PowerBI, Metabase).
- La publication en Open Data sur les portails publics (data.gouv.fr).
- L'auditabilité par des tiers (Sobriété numérique).

**Endpoints implémentés :**
- `GET /api/exports/kpis.csv` : Export tabulaire standardisé.
- `GET /api/kpis` : API JSON temps réel.
