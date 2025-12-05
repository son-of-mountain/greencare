# GreenCare - Santé Durable pour Demain

[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR-SITE-ID/deploy-status)](https://app.netlify.com/sites/YOUR-SITE-NAME/deploys)

## 🌱 Déploiement sur Netlify

### Option 1 : Déploiement automatique via GitHub (Recommandé)

1. **Connectez votre repository à Netlify** :
   - Allez sur [netlify.com](https://netlify.com) et connectez-vous
   - Cliquez sur "Add new site" → "Import an existing project"
   - Sélectionnez "GitHub" et autorisez Netlify
   - Choisissez le repository `greencare`

2. **Configuration du build** :
   - Build command: `echo 'No build needed'`
   - Publish directory: `frontend`
   - Cliquez sur "Deploy site"

3. **Configuration des variables d'environnement** (optionnel) :
   - Allez dans Site settings → Environment variables
   - Ajoutez vos variables si nécessaire

### Option 2 : Déploiement manuel avec Netlify CLI

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Se connecter à Netlify
netlify login

# Initialiser le site
netlify init

# Déployer
netlify deploy --prod --dir=frontend
```

### ⚠️ Note importante sur le Backend

Le backend FastAPI ne peut pas être hébergé directement sur Netlify (qui est pour les sites statiques). 

**Options pour le backend** :

1. **Render.com** (Gratuit) :
   ```bash
   # Créer un compte sur render.com
   # Connecter le repository
   # Créer un Web Service avec :
   # - Build Command: pip install -r backend/requirements.txt
   # - Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Railway.app** (Gratuit avec limitations) :
   ```bash
   # S'inscrire sur railway.app
   # Créer un nouveau projet depuis GitHub
   # Railway détectera automatiquement FastAPI
   ```

3. **Heroku** :
   ```bash
   # Créer un Procfile
   echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

### 📝 Configuration API après déploiement

Une fois le backend déployé, mettez à jour `API_URL` dans les fichiers frontend :
- `frontend/script.js`
- `frontend/news.js`

```javascript
const API_URL = 'https://your-backend-url.com/api';
```

## 🚀 Déploiement complet recommandé

1. **Frontend** → Netlify (gratuit)
2. **Backend** → Render.com (gratuit)
3. **Base de données** → SQLite embarqué ou PostgreSQL sur Render

## 📦 Structure du projet pour Netlify

```
GreenCare/
├── frontend/          # ← Déployé sur Netlify
│   ├── index.html
│   ├── landing.html
│   ├── style.css
│   └── ...
├── backend/           # ← À déployer séparément (Render/Railway)
│   ├── main.py
│   └── ...
└── netlify.toml      # Configuration Netlify
```

## 🔗 URLs après déploiement

- **Frontend** : `https://greencare.netlify.app`
- **Backend** : `https://greencare-api.onrender.com` (ou Railway/Heroku)

## 🛠️ Commandes utiles

```bash
# Déployer en production
netlify deploy --prod

# Tester en preview
netlify deploy

# Voir les logs
netlify logs

# Ouvrir le dashboard
netlify open
```

---

**Note** : Pour un projet full-stack avec FastAPI, je recommande plutôt **Render.com** ou **Railway.app** qui peuvent héberger le frontend ET le backend ensemble.
