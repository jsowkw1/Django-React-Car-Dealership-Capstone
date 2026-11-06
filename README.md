# Car Dealership Review Application

[![CI](https://github.com/jsowkw1/Django-React-Car-Dealership-Capstone/actions/workflows/ci.yml/badge.svg)](https://github.com/jsowkw1/Django-React-Car-Dealership-Capstone/actions/workflows/ci.yml)

Full-stack capstone project (IBM Full Stack Software Developer): a nationwide car-dealership
review site. Visitors browse dealerships and filter them by state; registered users post reviews,
which are automatically scored by a sentiment analyzer.

| Layer | Technology | Responsibility |
|-------|------------|----------------|
| Web app | **Django 5.1** (Python 3) | Auth (register / login / logout, sessions, hashed passwords), Django Admin, car makes & models, JSON API used by React, serves the React build |
| Frontend | **React 18 + React Router 6** (Vite) | Home / dealers / dealer details / post review / login / sign-up / About Us / Contact Us |
| Microservice | **Express 5 + Mongoose 9** (Node.js) | Dealers, reviews, state filter, sentiment analyzer |
| Database | **MongoDB** (Atlas or embedded `mongodb-memory-server`) + SQLite (Django) | Dealers & reviews in MongoDB; users and car makes/models in SQLite |
| CI/CD | **GitHub Actions** | Express tests, Django lint/checks/tests, React build, Docker image smoke test |
| Deployment | **Docker** + **Render** blueprint (`render.yaml`) | One container: gunicorn + Express + MongoDB |

```
Browser ──► Django (gunicorn, :8000) ──► Express API (:3030) ──► MongoDB
   ▲            │  /djangoapp/* JSON API        │  /fetchDealers, /fetchReviews, /insert_review
   │            │  /admin  (Django Admin)        │  /analyze/:text  (sentiment analyzer)
   └── React ◄──┘  React build served as static files
```

## Features
- 15 demonstration dealerships across 11 states (4 in Kansas), each with address, phone, description and photo.
- Dealer filtering by state (`/dealers/Kansas`) plus client-side search by name / city / ZIP.
- Dealer details with average rating, star ratings and per-review sentiment badges.
- Post Review form (logged-in users): review text, 1–5 star rating, purchase flag/date, car make/model/year.
- Registration with 5 fields (username, first name, last name, email, password) and server-side validation;
  login, logout alert, CSRF-protected session auth, Django password hashing and validators.
- Car makes (8) and car models (29) managed in Django Admin and exposed as JSON.
- Sentiment analyzer: AFINN-165 lexicon (npm `sentiment`), returns label, score and the words that drove it.
- About Us (fictional demo team with photos, roles, bios, emails) and Contact Us (details + form).

## Quick start (local)
Requirements: Python 3.11+, Node.js 20.19+ (22 LTS recommended). No MongoDB install needed.

```bash
git clone https://github.com/jsowkw1/Django-React-Car-Dealership-Capstone.git
cd Django-React-Car-Dealership-Capstone

# 1) Express + MongoDB API (embedded MongoDB is downloaded and seeded automatically)
cd express-api && npm install && npm start          # http://localhost:3030

# 2) React build (in a second terminal)
cd frontend && npm install && npm run build

# 3) Django (in a third terminal)
python -m venv .venv && .venv/Scripts/activate      # macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py seed_demo                          # root superuser, demo users, car makes/models
python manage.py runserver 8000                     # http://localhost:8000
```

Demonstration credentials (local only, created by `seed_demo` / the sign-up page):

| Account | Username | Password |
|---------|----------|----------|
| Django superuser | `root` | `Root@Admin2026` |
| Demo user | `demo_user` | `Demo@Pass2026` |
| Account registered in the screenshots | `jsowkw1` | `DriveSafe#2026` |

In production the superuser password comes from `DJANGO_SUPERUSER_PASSWORD`.

## Tests
```bash
cd express-api && npm test                        # 13 API tests (node:test + supertest + embedded MongoDB)
cd backend && python manage.py test djangoapp     # 22 Django tests
cd frontend && npm run build                      # production build
```

## Project structure
```
backend/            Django project (djangoproj/) and app (djangoapp/: models, views, admin, tests, seed command)
express-api/        Express API: models/, routes/, controllers/, middleware/, services/, seed/, tests/
frontend/           React app: src/components, src/pages, src/services, src/styles
scripts/            Screenshot automation, cURL example runner, production start script
screenshots/        Genuine screenshots for the peer-graded submission
submission/         Documentation and answers for the 28 tasks
.github/workflows/  CI pipeline
Dockerfile, render.yaml   Production container and Render blueprint
```

## Documentation
- [Project setup](submission/PROJECT_SETUP.md)
- [API documentation](submission/API_DOCUMENTATION.md)
- [cURL commands with actual outputs](submission/CURL_COMMANDS.md)
- [Test results](submission/TEST_RESULTS.md)
- [Deployment guide](submission/DEPLOYMENT_GUIDE.md)
- [Answers for all 28 tasks](submission/TASK_ANSWERS.md)
- [Screenshot checklist](submission/SCREENSHOT_CHECKLIST.md)

All dealer, review, team and contact data is fictional demonstration data. Photos are loaded from Unsplash.
