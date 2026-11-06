# Project setup

## Prerequisites
| Tool | Version used | Notes |
|------|--------------|-------|
| Python | 3.11 (local), 3.12 (CI / Docker) | |
| Node.js | 24 (local), 22 LTS (CI / Docker) | Express 5 / Mongoose 9 need ≥ 20.19 |
| MongoDB | none required | The API starts an embedded MongoDB (`mongodb-memory-server`) when `MONGODB_URI` is empty |
| Git | any | |

## 1. Express + MongoDB API
```bash
cd server/database
npm install
cp .env.example .env            # optional; defaults work
npm start                       # → [api] Express API listening on http://localhost:3030
```
On first start the database is empty, so the server seeds 15 dealerships and 14 reviews from
`seed/dealerships.json` and `seed/reviews.json`.

- Persist embedded data between restarts: `MONGO_DATA_DIR=./.mongo-data npm start`
- Use a real MongoDB / Atlas: `MONGODB_URI="mongodb+srv://..." npm start`
- Reset the data at any time: `npm run seed` (same `MONGODB_URI` / `MONGO_DATA_DIR` as the server, with the server stopped when using `MONGO_DATA_DIR`)

## 2. React frontend
```bash
cd server/frontend
npm install
npm run build                   # → server/frontend/dist (served by Django under /static/)
```
For hot-reload development run `npm run dev` (http://localhost:5173); `/djangoapp` and `/admin`
requests are proxied to Django on port 8000.

## 3. Django
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r server/requirements.txt
cd server
cp ../.env.example .env         # optional
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8000
```
Open http://localhost:8000.

`seed_demo` is idempotent and creates:
- superuser `root` (password `Root@Admin2026`, or `DJANGO_SUPERUSER_PASSWORD`)
- demo users `demo_user`, `emily_carter`, `marcus_lee` (password `Demo@Pass2026`, or `DEMO_USER_PASSWORD`)
- 8 car makes and 29 car models (also auto-populated on the first `/djangoapp/get_cars` call)

## Environment variables
| Variable | Service | Default | Purpose |
|----------|---------|---------|---------|
| `DJANGO_SECRET_KEY` | Django | dev key when `DEBUG=True` | Required in production |
| `DEBUG` | Django | `True` | `False` in production |
| `ALLOWED_HOSTS` | Django | `localhost,127.0.0.1,[::1]` | Render hostname is added automatically |
| `CSRF_TRUSTED_ORIGINS` | Django | empty | e.g. `https://my-app.onrender.com` |
| `BACKEND_URL` | Django | `http://localhost:3030` | Express API base URL |
| `SENTIMENT_ANALYZER_URL` | Django | `BACKEND_URL` | Sentiment analyzer base URL |
| `EXPRESS_API_KEY` | Django | empty | Sent as `X-API-Key` when posting reviews |
| `PORT` | Express | `3030` | |
| `MONGODB_URI` | Express | empty → embedded | MongoDB connection string |
| `MONGO_DATA_DIR` | Express | empty | Persist embedded MongoDB data |
| `API_KEY` | Express | empty | Require `X-API-Key` on `POST /insert_review` |

Secrets are never committed; see `.env.example` and `server/database/.env.example`.

## Useful URLs (local)
| URL | What |
|-----|------|
| http://localhost:8000/ | Home page with dealers |
| http://localhost:8000/dealers/Kansas | Dealers filtered by state |
| http://localhost:8000/dealer/1 | Dealer details and reviews |
| http://localhost:8000/postreview/1 | Post a review (logged in) |
| http://localhost:8000/about, /contact, /login, /register | Static pages and auth |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/djangoapp/get_cars | Car makes and models (JSON) |
| http://localhost:3030/fetchDealers | Express: all dealers |
| http://localhost:3030/analyze/Fantastic%20services | Sentiment analyzer |

## Regenerating the evidence (Windows)
```bash
python scripts/capture_terminal.py                 # Task 2: opens a console running runserver and captures it
python scripts/capture_screenshots.py local        # Tasks 3–22 from a real Chrome window
python scripts/run_curl_examples.py                # submission/CURL_COMMANDS.md with real outputs
python scripts/capture_screenshots.py github       # Task 23 (GitHub Actions page)
python scripts/capture_screenshots.py deployed --base https://<app>.onrender.com --api https://<app>.onrender.com/djangoapp
```
