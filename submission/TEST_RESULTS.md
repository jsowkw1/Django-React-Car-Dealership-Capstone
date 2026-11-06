# Test results

All results below are real outputs from runs on 2026-11-06 on the development machine
(Windows 11, Python 3.11.1, Node.js 24.11.1). The same suites run in GitHub Actions on every push
(see Task 23 and `.github/workflows/ci.yml`).

## Summary
| Area | Command | Result |
|------|---------|--------|
| Express API (13 tests) | `cd server/database && npm test` | 13 passed, 0 failed |
| Django system checks | `python manage.py check` | no issues |
| Django deploy checks (DEBUG=False) | `python manage.py check --deploy --fail-level ERROR` | passed (warnings only: HSTS/SSL-redirect left to the hosting proxy) |
| Django migrations | `python manage.py makemigrations --check --dry-run` | No changes detected |
| Django tests (22 tests) | `python manage.py test djangoapp` | 22 passed (also passed with DEBUG=False) |
| Lint | `flake8 djangoapp djangoproj --max-line-length=130 --exclude=migrations` | no findings |
| Frontend production build | `cd server/frontend && npm run build` | built successfully |
| End-to-end (browser) | `python scripts/capture_screenshots.py local` | full flow passed: register → home → logout → login → filter by state → dealer details → post review → review shown → Express endpoints → Django admin login/car makes/car models/logout |
| API via cURL | `python scripts/run_curl_examples.py` | 26 requests, every status code as expected (200/201/400/401/404), see CURL_COMMANDS.md |

## Feature coverage
| Feature | Covered by |
|---------|-----------|
| Django system checks / migrations | `manage.py check`, `makemigrations --check`, CI |
| Registration (5 fields, validation, password hashing) | `test_register_creates_user_and_logs_in`, `test_register_validation_errors`, e2e Task 7 |
| Login / logout / sessions / CSRF | `test_login_success_and_failure`, `test_logout`, `test_csrf_is_enforced`, e2e Tasks 5–6 |
| Dealer retrieval / filtering / details | Express tests 2–6, `DealerProxyTests`, e2e Tasks 17–20 |
| Review submission and retrieval | `POST /insert_review` tests, `AddReviewTests`, e2e Tasks 21–22 |
| Car makes / models | `CarTests`, e2e Tasks 14–15 |
| Sentiment analysis (`Fantastic services` → positive) | Express sentiment tests, `SentimentClientTests`, Task 16 |
| Frontend build | `npm run build`, CI job |
| GitHub Actions | CI run #1 (42205357737): all 4 jobs passed, including the Docker image smoke test that builds the production image, starts it and checks `/`, Kansas dealers, reviews, `Fantastic services` sentiment, car models and static files |

## Express API — `npm test`
```
> dealership-express-api@1.0.0 test
> node --test --test-concurrency=1 tests/api.test.js

[db] Embedded MongoDB started at mongodb://127.0.0.1:58752/
[db] Connected to MongoDB
✔ GET / returns the service index (1105.5027ms)
✔ GET /fetchDealers returns all seeded dealers (31.6737ms)
✔ GET /fetchDealers/Kansas filters by full state name (18.3791ms)
✔ GET /fetchDealers/ks filters by state code, case-insensitive (21.3864ms)
✔ GET /fetchDealers/Atlantis returns an empty list (15.8624ms)
✔ GET /fetchDealer/:id returns one dealer, 404 and 400 on bad ids (37.9868ms)
✔ GET /fetchReviews/dealer/1 returns multiple reviews with sentiment (17.285ms)
✔ POST /insert_review creates a review (201) and it is retrievable (61.6961ms)
✔ POST /insert_review validates input (400) and unknown dealer (404) (23.5106ms)
✔ POST /insert_review requires X-API-Key when API_KEY is set (401) (28.6616ms)
✔ GET /analyze/Fantastic services is positive (14.4087ms)
✔ sentiment analyzer handles negative and neutral text (26.0812ms)
✔ unknown routes return a JSON 404 (14.5187ms)
ℹ tests 13
ℹ suites 0
ℹ pass 13
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 3625.7617
```

## Django — `python manage.py check`
```
System check identified no issues (0 silenced).
```

## Django — `python manage.py test djangoapp -v 2`
```
Found 22 test(s).
System check identified no issues (0 silenced).
test_posts_review_to_express ... ok
test_requires_login ... ok
test_validation ... ok
test_csrf_is_enforced ... ok
test_login_rejects_bad_json ... ok
test_login_success_and_failure ... ok
test_logout ... ok
test_register_creates_user_and_logs_in ... ok
test_register_validation_errors ... ok
test_car_makes_and_filtered_models ... ok
test_get_cars_populates_and_lists ... ok
test_seed_is_idempotent ... ok
test_backend_unavailable ... ok
test_dealer_details ... ok
test_dealer_not_found ... ok
test_get_dealers ... ok
test_get_dealers_by_state ... ok
test_reviews_get_sentiment_and_average ... ok
test_admin_login_page ... ok
test_spa_routes_resolve ... ok
test_analyze_url_encodes_text ... ok
test_analyzer_down_falls_back_to_neutral ... ok
Ran 22 tests in 14.945s
OK
```

## Frontend — `npm run build`
```
> dealership-frontend@1.0.0 build
> vite build
vite v6.0.7 building for production...
transforming...
✓ 46 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.89 kB │ gzip:  0.47 kB
dist/assets/index-IOdRRy6W.css   11.45 kB │ gzip:  3.45 kB
dist/assets/index-DRBPJGxa.js   193.53 kB │ gzip: 62.26 kB
✓ built in 1.13s
```
