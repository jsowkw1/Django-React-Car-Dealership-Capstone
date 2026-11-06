# Answers for the 28 peer-graded tasks (upload in this order)

Status legend: ✅ done and verified · ⏳ waiting for a manual step (see the end of this file)

---
**TASK 1 — GitHub repository URL** ✅
Answer: `https://github.com/jsowkw1/Django-React-Car-Dealership-Capstone`
Verified: public repository, all source code pushed to `main`.

**TASK 2 — Django server running** ✅
Screenshot: `screenshots/task02_django_server.png`. Console output of `python manage.py runserver 8000`: "System check identified no issues", Django 5.1.15, "Starting development server at http://127.0.0.1:8000/".

**TASK 3 — About Us page** ✅
Screenshot: `screenshots/task03_about_us.png`; full team cards in `task03_about_us_team.png`. URL `localhost:8000/about`, styled page, About Us active in the navbar, 4 team members with photo, name, role, description and email (fictional demo team).

**TASK 4 — Contact Us page** ✅
Screenshot: `screenshots/task04_contact_us.png`. URL `localhost:8000/contact`, navbar with **Contact Us** active, images, address, phone, emails, opening hours, contact form.

**TASK 5 — Login page** ✅
Screenshot: `screenshots/task05_login.png` (form filled in). `task05_login_success.png` shows the result: user `jsowkw1` logged in.

**TASK 6 — Logout alert** ✅
Screenshot: `screenshots/task06_logout.png`, the browser alert "localhost:8000 says: Logging out jsowkw1...". `task06_logout_confirmation.png` shows the success banner that follows.

**TASK 7 — Sign-up page** ✅
Screenshot: `screenshots/task07_signup.png`. Fields: Username, First Name, Last Name, Email, Password, plus the Register button. Registration was submitted and created the account (see Task 18).

**TASK 8 — Dealer reviews (Express-Mongo endpoint)** ✅
Screenshot: `screenshots/task08_dealer_reviews.png`. URL `http://localhost:3030/fetchReviews/dealer/1` (dealer 1 has several reviews).

**TASK 9 — All dealers (Express-Mongo endpoint)** ✅
Screenshot: `screenshots/task09_all_dealers.png`. URL `http://localhost:3030/fetchDealers`.

**TASK 10 — Dealer details (Express-Mongo endpoint)** ✅
Screenshot: `screenshots/task10_dealer_details_api.png`. URL `http://localhost:3030/fetchDealer/3`.

**TASK 11 — Dealers in Kansas** ✅
Screenshot: `screenshots/task11_kansas_dealers.png`. URL `http://localhost:3030/fetchDealers/Kansas`, 4 dealers.

**TASK 12 — Django admin login** ✅
Screenshot: `screenshots/task12_admin_login.png`. `localhost:8000/admin/` showing "Welcome, root".

**TASK 13 — Django admin logout** ✅
Screenshot: `screenshots/task13_admin_logout.png`. `localhost:8000/admin/logout/` showing "Logged out".

**TASK 14 — Car makes** ✅
Screenshot: `screenshots/task14_car_makes.png`. URL `localhost:8000/admin/djangoapp/carmake/`: 8 makes (BMW, Chevrolet, Ford, Honda, Mercedes-Benz, Nissan, Subaru, Toyota). JSON endpoint: `task14_car_makes_api.png` (`/djangoapp/get_cars`).

**TASK 15 — Car models** ✅
Screenshot: `screenshots/task15_car_models.png`. URL `localhost:8000/admin/djangoapp/carmodel/`, 29 models with make, type, year and dealer id.

**TASK 16 — Sentiment analyzer (deployed URL)** ✅
Screenshot: `screenshots/task16_sentiment_analyzer.png`. URL `https://bestcars-dealership-i2j9.onrender.com/djangoapp/analyze/Fantastic%20services` → `"sentiment": "positive"`, score 4, positive word "fantastic". Local Express endpoint: `task16_sentiment_analyzer_local.png`.

**TASK 17 — Homepage before login** ✅
Screenshot: `screenshots/task17_homepage_guest.png`. URL `localhost:8000`, dealer cards, Login/Register in the navbar.

**TASK 18 — Homepage after login** ✅
Screenshot: `screenshots/task18_homepage_loggedin.png`. URL `localhost:8000`, username `jsowkw1` in the navbar, **Post Review** buttons on every dealer.

**TASK 19 — Dealers filtered by state** ✅
Screenshot: `screenshots/task19_dealers_by_state.png`. URL `localhost:8000/dealers/Kansas`, "Dealerships in Kansas: 4 dealerships found".

**TASK 20 — Dealer details and reviews** ✅
Screenshot: `screenshots/task20_dealer_details_reviews.png`. URL `localhost:8000/dealer/1`: address, phone, 4.7/5 rating, 3 reviews with sentiment.

**TASK 21 — Add review (before submitting)** ✅
Screenshot: `screenshots/task21_review_submission.png`. URL `localhost:8000/postreview/1`. Review: "Fantastic services! Friendly staff, a quick test drive and transparent pricing on my new Camry.", 5 stars, purchased 10/25/2026, Toyota Camry (2025).

**TASK 22 — Added review** ✅
Screenshot: `screenshots/task22_added_review.png`. URL `localhost:8000/dealer/1`. The new review by Capstone Reviewer (`jsowkw1`) is highlighted with the same text, 5 stars, purchase date 2026-10-25 and Toyota Camry 2025, marked Positive.

**TASK 23 — GitHub Actions CI/CD** ✅
Screenshot: `screenshots/task23_github_actions.png`. Run #1 of workflow "CI" at `github.com/jsowkw1/Django-React-Car-Dealership-Capstone/actions/runs/42205357737`: Status **Success**, all 4 jobs green (Express API tests, React production build, Django checks and tests, Production image smoke test). The Actions list is in `task23_github_actions_list.png`.
Workflow: `.github/workflows/ci.yml` (Express tests, React build, Django lint/checks/migrations/tests, Docker image smoke test).

**TASK 24 — Deployment URL** ✅
Answer: `https://bestcars-dealership-i2j9.onrender.com`
(Render free web service `bestcars-dealership`, Docker image from this repository, deployed from `render.yaml`. It sleeps after inactivity, so the first request can take about a minute.)

**TASK 25 — Deployed landing page** ✅
Screenshot: `screenshots/task25_deployed_landingpage.png`. URL `https://bestcars-dealership-i2j9.onrender.com`, hero and dealer list, logged out.

**TASK 26 — Deployed logged-in page** ✅
Screenshot: `screenshots/task26_deployed_loggedin.png`. URL `https://bestcars-dealership-i2j9.onrender.com`, `jsowkw1` in the navbar, Post Review buttons.

**TASK 27 — Deployed dealer details** ✅
Screenshot: `screenshots/task27_deployed_dealer_detail.png`. URL `https://bestcars-dealership-i2j9.onrender.com/dealer/3`, Prairie Village Premium Cars, details, rating and 2 reviews.

**TASK 28 — Deployed added review** ✅
Screenshot: `screenshots/task28_deployed_add_review.png`. URL `https://bestcars-dealership-i2j9.onrender.com/dealer/3`, the new review by Capstone Reviewer (jsowkw1) is highlighted: "Deployed test: fantastic services and a very helpful, friendly team.", 5 stars, BMW X5 2026, Positive. Reviews (3).

---
## Status
All 28 tasks are complete and verified. No manual steps remain.
Note: the free Render instance uses the embedded MongoDB, so reviews posted on the live site reset when the service restarts (the seed data comes back automatically).
