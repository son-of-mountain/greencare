# --- STAGE 1 : Builder (Compilation) ---
FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Création d'un environnement virtuel (venv) pour isoler les dépendances
RUN python -m venv /opt/venv
# On active l'environnement virtuel pour les prochaines commandes
ENV PATH="/opt/venv/bin:$PATH"

COPY ./backend/requirements.txt .
# Installation dans le venv
RUN pip install --no-cache-dir -r requirements.txt

# --- STAGE 2 : Runner (Image finale) ---
FROM python:3.10-slim

WORKDIR /app

# Création utilisateur non-root
RUN addgroup --system numih && adduser --system --group numih

# Copie de l'environnement virtuel complet depuis le builder
# C'est ici que la magie opère : on récupère tout (binaires + libs) d'un coup
COPY --from=builder /opt/venv /opt/venv

# Activation du venv dans l'image finale
ENV PATH="/opt/venv/bin:$PATH"

# Copie du code source avec les bonnes permissions
COPY --chown=numih:numih ./backend /app/backend
COPY --chown=numih:numih ./frontend /app/frontend

# Dossier pour la DB SQLite
RUN mkdir /app/data && chown numih:numih /app/data

# Passage utilisateur non-root
USER numih

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
