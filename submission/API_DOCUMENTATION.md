# API documentation

Two JSON APIs make up the backend:

1. **Express + MongoDB API** (`server/database/`, default `http://localhost:3030`): owns dealers, reviews and the sentiment analyzer.
2. **Django API** (`server/djangoapp/`, `http://localhost:8000/djangoapp/`): authentication, car makes/models, and proxies
   to the Express API for the React frontend.

Real requests and responses for every endpoint are in [CURL_COMMANDS.md](CURL_COMMANDS.md).

## Response conventions
- Successful `GET` requests on the Express API return the resource itself (an array of dealers / reviews or a dealer object).
- Django endpoints wrap results: `{"status": 200, "count": n, "dealers": [...]}`.
- Errors always have the shape `{"status": <code>, "error": "<message>"}` (Django validation errors add an `errors` object per field).

| Code | When |
|------|------|
| 200 OK | Successful read, login, logout |
| 201 Created | Review inserted, user registered |
| 400 Bad Request | Invalid id, malformed JSON, failed validation |
| 401 Unauthorized | Wrong credentials, posting a review while logged out, missing/invalid `X-API-Key` |
| 403 Forbidden | Django CSRF check failed (missing `X-CSRFToken` header on a POST) |
| 404 Not Found | Unknown dealer or route |
| 500 Internal Server Error | Unexpected server error (message hidden from clients, logged on the server) |
| 503 Service Unavailable | Django cannot reach the Express API |

## Express + MongoDB API

| # | Method & path | Description | Success | Errors |
|---|---------------|-------------|---------|--------|
| 1 | `GET /fetchDealers` | All dealers sorted by id | 200 array | 500 |
| 2 | `GET /fetchDealer/:id` | One dealer by numeric id | 200 object | 400 invalid id, 404 |
| 3 | `GET /fetchDealers/:state` | Dealers in a state; full name (`Kansas`) or code (`KS`), case-insensitive | 200 array (may be empty) | 400 |
| 4 | `GET /fetchReviews/dealer/:id` | Reviews of a dealer, newest first | 200 array | 400 |
| – | `GET /fetchReviews` | All reviews | 200 array | |
| – | `POST /insert_review` | Create a review (JSON body below). Requires `X-API-Key` when `API_KEY` is set | 201 review | 400, 401, 404 dealer |
| 7 | `GET /analyze/:text` | Sentiment of URL-encoded text | 200 | 400 empty |
| 7 | `POST /analyze` | Sentiment of `{"text": "..."}` | 200 | 400 |
| – | `GET /` | Service index / health | 200 | |

### Dealer object
```json
{ "id": 1, "full_name": "Sunflower State Motors", "short_name": "Sunflower Motors",
  "address": "2450 N Rock Rd", "city": "Wichita", "state": "Kansas", "st": "KS", "zip": "67226",
  "lat": 37.7303, "long": -97.2457, "phone": "(316) 555-0141",
  "description": "Family-owned since 1998, ...", "image": "https://images.unsplash.com/..." }
```

### Review object / `POST /insert_review` body
| Field | Type | Required | Rules |
|-------|------|----------|-------|
| `name` | string | yes | reviewer display name |
| `dealership` | integer | yes | must be an existing dealer id |
| `review` | string | yes | 1–2000 characters |
| `rating` | integer | yes | 1–5 |
| `purchase` | boolean | no | |
| `purchase_date` | string | no | `YYYY-MM-DD` |
| `car_make`, `car_model` | string | no | |
| `car_year` | integer | no | 1950–2030 |

The server adds `id` (next integer), `sentiment` (computed from the review text) and `created_at`.

### Sentiment analyzer
Implementation: `server/database/services/sentiment.js`, using the AFINN-165 word list (npm package `sentiment`,
which also handles negation such as "not good"). Each known word scores −5…+5; `comparative` = total score ÷ number
of words. Label: `positive` if comparative > 0.05, `negative` if < −0.05, otherwise `neutral`. Nothing is hard-coded
for particular phrases.

```json
GET /analyze/Fantastic%20services
{ "text": "Fantastic services", "sentiment": "positive", "score": 4, "comparative": 2,
  "positive_words": ["fantastic"], "negative_words": [], "analyzer": "AFINN-165 lexicon (npm sentiment)" }
```

## Django API (`/djangoapp/`)
All `POST` endpoints need the `csrftoken` cookie (set by any page or `GET /djangoapp/me`) echoed in the
`X-CSRFToken` header, as the React app does.

| Method & path | Auth | Description |
|---------------|------|-------------|
| `GET /djangoapp/me` | – | Current user (`isAuthenticated`, `userName`, names, email); sets CSRF cookie |
| `POST /djangoapp/register` | – | Body `{userName, firstName, lastName, email, password}` → 201 and logged in; 400 with per-field `errors` |
| `POST /djangoapp/login` | – | Body `{userName, password}` → 200 / 401 |
| `POST /djangoapp/logout` | – | Ends the session → 200 |
| `GET /djangoapp/get_dealers` | – | All dealers (from Express) |
| `GET /djangoapp/get_dealers/<state>` | – | Dealers by state |
| `GET /djangoapp/dealer/<id>` | – | Dealer details (404 if unknown) |
| `GET /djangoapp/reviews/dealer/<id>` | – | Reviews with `sentiment` and `average_rating` |
| `POST /djangoapp/add_review` | **login** | Body `{dealership, review, rating, purchase, purchase_date, car_id \| car_make+car_model+car_year}` → 201; 401 if logged out; 400 validation |
| `GET /djangoapp/analyze/<text>` | – | Sentiment analyzer (proxied) |
| `GET /djangoapp/get_cars` | – | All car models with their make (course format `CarModel` / `CarMake`) |
| `GET /djangoapp/get_car_makes` | – | Car makes with country, founding year and model names |
| `GET /djangoapp/get_car_models?make=<name>` | – | Car models, optionally filtered by make |

## Django models
- `CarMake`: `name` (unique), `description`, `country`, `founded`
- `CarModel`: `car_make` (FK), `name`, `type` (Sedan, SUV, Wagon, Truck, Coupe, Hatchback, Electric), `year` (2015–2026), `dealer_id`
- Users: `django.contrib.auth.models.User` (PBKDF2-SHA256 hashed passwords)
