# Screenshot checklist

All screenshots are genuine captures of a real, visible Google Chrome window (address bar included) or a real
Windows console window, taken by `scripts/capture_screenshots.py` / `scripts/capture_terminal.py`.
Nothing is drawn, edited or composited. Files live in [`screenshots/`](../screenshots).

| Task | File | Shows | Status |
|------|------|-------|--------|
| 2 | `task02_django_server.png` | Console running `python manage.py runserver 8000`: system checks, Django 5.1.15, `Starting development server at http://127.0.0.1:8000/` | ✅ captured |
| 3 | `task03_about_us.png` (+ `task03_about_us_team.png`) | About Us at `localhost:8000/about`, navbar with About Us active, values, 4 team members with photos, names, roles, bios, emails | ✅ captured |
| 4 | `task04_contact_us.png` | Contact Us at `localhost:8000/contact`, navbar with **Contact Us** active, image, contact details, form | ✅ captured |
| 5 | `task05_login.png` (+ `task05_login_success.png`) | Login form filled in; after submit the navbar shows `jsowkw1` | ✅ captured |
| 6 | `task06_logout.png` (+ `task06_logout_confirmation.png`) | Browser alert "Logging out jsowkw1..." and the "logged out successfully" banner | ✅ captured |
| 7 | `task07_signup.png` | Sign Up page with the 5 fields (Username, First Name, Last Name, Email, Password) filled in and the Register button | ✅ captured |
| 8 | `task08_dealer_reviews.png` | `localhost:3030/fetchReviews/dealer/1` (dealer with several reviews) | ✅ captured |
| 9 | `task09_all_dealers.png` | `localhost:3030/fetchDealers` | ✅ captured |
| 10 | `task10_dealer_details_api.png` | `localhost:3030/fetchDealer/3` | ✅ captured |
| 11 | `task11_kansas_dealers.png` | `localhost:3030/fetchDealers/Kansas` | ✅ captured |
| 12 | `task12_admin_login.png` | Django Admin index, "WELCOME, ROOT" | ✅ captured |
| 13 | `task13_admin_logout.png` | Django Admin "Logged out" page at `/admin/logout/` | ✅ captured |
| 14 | `task14_car_makes.png` (+ `task14_car_makes_api.png`) | Admin list of 8 car makes at `/admin/djangoapp/carmake/`; JSON at `/djangoapp/get_cars` | ✅ captured |
| 15 | `task15_car_models.png` | Admin list of 29 car models at `/admin/djangoapp/carmodel/` | ✅ captured |
| 16 | `task16_sentiment_analyzer.png` | Sentiment analyzer for "Fantastic services" on the **deployed** URL | ⏳ pending deployment (local evidence: `task16_sentiment_analyzer_local.png`) |
| 17 | `task17_homepage_guest.png` | Dealers on `localhost:8000/` before login (Login/Register in navbar) | ✅ captured |
| 18 | `task18_homepage_loggedin.png` | Dealers after login: `jsowkw1` in navbar and **Post Review** buttons | ✅ captured |
| 19 | `task19_dealers_by_state.png` | `localhost:8000/dealers/Kansas`, "Dealerships in Kansas", 4 dealers | ✅ captured |
| 20 | `task20_dealer_details_reviews.png` | `localhost:8000/dealer/1`: details, rating, reviews with sentiment | ✅ captured |
| 21 | `task21_review_submission.png` | `localhost:8000/postreview/1`, form filled (text, 5 stars, purchase date, Toyota Camry 2025) before submitting | ✅ captured |
| 22 | `task22_added_review.png` | `localhost:8000/dealer/1` with the new review (same text, rating, car, date) highlighted | ✅ captured |
| 23 | `task23_github_actions.png` (+ `task23_github_actions_list.png`) | CI run #1 at `github.com/jsowkw1/Django-React-Car-Dealership-Capstone/actions/runs/42205357737`: Success, 4/4 jobs green | ✅ captured |
| 25 | `task25_deployed_landingpage.png` | Deployed landing page | ⏳ pending deployment |
| 26 | `task26_deployed_loggedin.png` | Deployed home page logged in (`jsowkw1`) | ⏳ pending deployment |
| 27 | `task27_deployed_dealer_detail.png` | Deployed dealer details | ⏳ pending deployment |
| 28 | `task28_deployed_add_review.png` | Review added on the deployed app | ⏳ pending deployment |

Tasks 1 and 24 are URLs, not screenshots.
