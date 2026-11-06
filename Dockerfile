# Single-container production image: Django (gunicorn) + React build + Express API + MongoDB.
# Django serves the site on $PORT; Express runs on localhost:3030 inside the container and uses
# MONGODB_URI if provided (e.g. MongoDB Atlas) or an embedded MongoDB otherwise.

# ---------- React build ----------
FROM node:22-bookworm-slim AS frontend
WORKDIR /app/server/frontend
COPY server/frontend/package.json server/frontend/package-lock.json ./
RUN npm ci
COPY server/frontend/ ./
RUN npm run build

# ---------- Express dependencies (also downloads the embedded MongoDB binary for Debian 12) ----------
FROM node:22-bookworm-slim AS api
WORKDIR /app/server/database
COPY server/database/package.json server/database/package-lock.json ./
RUN npm ci --omit=dev
COPY server/database/ ./

# ---------- Runtime ----------
FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False \
    PORT=8000 \
    SQLITE_PATH=/app/data/db.sqlite3 \
    BACKEND_URL=http://127.0.0.1:3030 \
    MONGO_CACHE_GB=0.25
RUN apt-get update \
    && apt-get install -y --no-install-recommends libcurl4 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=node:22-bookworm-slim /usr/local/bin/node /usr/local/bin/node
WORKDIR /app
COPY server/requirements.txt server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt
COPY server/manage.py server/
COPY server/djangoproj server/djangoproj
COPY server/djangoapp server/djangoapp
COPY server/frontend/static server/frontend/static
COPY --from=frontend /app/server/frontend/dist server/frontend/dist
COPY --from=api /app/server/database server/database
COPY scripts/start-production.sh scripts/start-production.sh
RUN mkdir -p /app/data \
    && cd server && DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput \
    && useradd --create-home appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["sh", "/app/scripts/start-production.sh"]
