# Utilisation de python slim (base Debian allégée) pour compatibilité maximale et taille réduite
# Alpine peut poser des soucis de compilation avec certaines libs Python sur Alma/RHEL hosts
FROM python:3.10-slim

# Variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système minimales si nécessaire
# (Pour le moment aucune, on garde l'image légère)

# Copie des requirements et installation
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code backend
COPY ./backend /app/backend

# Création d'un utilisateur non-root pour la sécurité (HDS requirement)
RUN adduser --disabled-password --gecos "" numihuser
USER numihuser

# Exposition du port
EXPOSE 8000

# Lancement
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
