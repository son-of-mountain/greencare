# Conformité HDS & Souveraineté (SecNumCloud)

GreenCare est conçu nativement pour s'intégrer dans l'environnement de confiance de **Numih France**.

## 1. Souveraineté des Données
- [cite_start]**Hébergement :** L'application est conteneurisée (Docker) pour être déployée exclusivement sur les datacenters Numih certifiés **HDS** (Amiens, Rennes, Toulouse)[cite: 142, 153].
- **Indépendance :** Aucune dépendance critique vers des API extra-européennes (GAFAM). Les bibliothèques frontend sont servies localement (pas de CDN tiers).
- **Législation :** Données soumises exclusivement au droit français et européen (RGPD), à l'abri des lois extraterritoriales (Cloud Act).

## 2. Sécurité Applicative (Security by Design)
- **HTTPS Force :** En production, tout trafic HTTP est redirigé vers HTTPS (TLS 1.2+).
- **Headers de Sécurité :**
  - `HSTS` : Force le chiffrement.
  - `Content-Security-Policy (CSP)` : Bloque les scripts tiers et traceurs.
  - `X-Frame-Options` : Empêche le clickjacking.
- **Minimisation :** Aucune donnée patient nominative n'est stockée dans ce module (uniquement des statistiques agrégées et annuaires pro).

## 3. Gestion des Logs
- Les logs applicatifs ne contiennent aucune donnée personnelle identifiante (PII).
- Rotation des logs configurée pour éviter la saturation (Sobriété).
