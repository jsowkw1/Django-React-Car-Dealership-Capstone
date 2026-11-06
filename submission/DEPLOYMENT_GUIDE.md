# Deployment guide

**Live deployment:** https://bestcars-dealership-i2j9.onrender.com (Render Blueprint `bestcars-capstone`, service `bestcars-dealership`, verified on 2026-11-06)

## Chosen hosting
| Component | Where it runs | Why |
|-----------|---------------|-----|
| Django + React build | Render free web service (Docker) | Free, deploys straight from GitHub with `render.yaml`, HTTPS URL |
| Express API | Same container, `127.0.0.1:3030` | No second service or cross-service networking needed |
| MongoDB | Embedded `mongodb-memory-server` in the container, **or** MongoDB Atlas (free M0) via `MONGODB_URI` | Embedded needs no account; Atlas keeps reviews across restarts |
| Django database | SQLite in the container | Users, sessions, car makes/models; recreated and re-seeded on start |

Alternatives that also work with the same `Dockerfile`: Koyeb, Fly.io, Railway, Google Cloud Run, IBM Code Engine.

Free-tier caveats (Render): the service sleeps after ~15 minutes without traffic and takes ~1 minute to wake up.
Without `MONGODB_URI`, the container filesystem is ephemeral, so registered users and posted reviews are
reset when the service restarts (seed data is recreated automatically).

## Production configuration
- `Dockerfile`: three stages (React build → Express deps incl. MongoDB binary → Python runtime), runs as a non-root user.
- `scripts/start-production.sh`: starts Express, runs `migrate` and `seed_demo`, then `gunicorn`.
- `render.yaml`: free Docker web service, health check `/djangoapp/me`, generated secrets.
- Django production settings: `DEBUG=False`, secret key from env, `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` include the
  Render hostname automatically (`RENDER_EXTERNAL_HOSTNAME`), secure cookies, WhiteNoise compressed static files,
  `SECURE_PROXY_SSL_HEADER` for HTTPS behind Render's proxy.
- The CI workflow builds this exact image, runs it and checks the main endpoints (job "Production image smoke test").

## Steps (Render)
1. Sign in at https://dashboard.render.com with the GitHub account `jsowkw1` (free, no card needed for free web services).
2. **New → Blueprint**, pick the repository `jsowkw1/Django-React-Car-Dealership-Capstone`, branch `main`.
3. Render reads `render.yaml`. When asked for `MONGODB_URI`, either leave it empty (embedded MongoDB) or paste an
   Atlas connection string.
4. Click **Apply**. The first build takes about 5 minutes. The URL looks like `https://bestcars-dealership-xxxx.onrender.com`.
5. Admin password for `root`: Render dashboard → service → **Environment** → `DJANGO_SUPERUSER_PASSWORD`.

### Optional: MongoDB Atlas
1. Create a free M0 cluster at https://www.mongodb.com/cloud/atlas.
2. Database Access → add a user; Network Access → allow `0.0.0.0/0`.
3. Copy the `mongodb+srv://...` string into the service's `MONGODB_URI` environment variable and redeploy.
   The API seeds the empty database on first start.

## Verifying the deployment
```bash
BASE=https://<your-service>.onrender.com
curl -s $BASE/djangoapp/get_dealers/Kansas
curl -s "$BASE/djangoapp/analyze/Fantastic%20services"
curl -s $BASE/djangoapp/reviews/dealer/3
```
Then capture Tasks 16 and 25–28 (Windows):
```bash
python scripts/capture_screenshots.py deployed --base $BASE --api $BASE/djangoapp
```
