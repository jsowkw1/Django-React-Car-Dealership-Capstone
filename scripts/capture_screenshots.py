"""Captures the submission screenshots from a real, visible Chrome window (address bar included).

Usage (Windows, app running locally):
    python scripts/capture_screenshots.py local
    python scripts/capture_screenshots.py deployed --base https://<your-app>.onrender.com --api https://<your-api>.onrender.com
    python scripts/capture_screenshots.py github --repo jsowkw1/Django-React-Car-Dealership-Capstone

Every image is a genuine capture of the browser window; nothing is drawn or edited.
Credentials are read from environment variables (demo defaults are documented in submission/).
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import date, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from wincap import browser_pids, capture_window, find_window  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / 'screenshots'
PROFILE_MARKER = 'capstone-shot-profile'

USER = {
    'userName': os.getenv('DEMO_USERNAME', 'jsowkw1'),
    'firstName': os.getenv('DEMO_FIRST_NAME', 'Capstone'),
    'lastName': os.getenv('DEMO_LAST_NAME', 'Reviewer'),
    'email': os.getenv('DEMO_EMAIL', 'jsowkw1.demo@example.com'),
    'password': os.getenv('DEMO_PASSWORD', 'DriveSafe#2026'),
}
ADMIN = (os.getenv('ADMIN_USERNAME', 'root'), os.getenv('ADMIN_PASSWORD', 'Root@Admin2026'))
REVIEW_TEXT = os.getenv(
    'REVIEW_TEXT',
    'Fantastic services! Friendly staff, a quick test drive and transparent pricing on my new Camry.',
)


class Shooter:
    def __init__(self, pw):
        # Fresh throw-away profile each run (default zoom, no saved sessions, no password prompts).
        profile = Path(tempfile.gettempdir()) / PROFILE_MARKER
        shutil.rmtree(profile, ignore_errors=True)
        (profile / 'Default').mkdir(parents=True)
        (profile / 'Default' / 'Preferences').write_text(json.dumps({
            'credentials_enable_service': False,
            'profile': {'password_manager_enabled': False, 'default_zoom_level': 0},
            'translate': {'enabled': False},
        }))
        self.ctx = pw.chromium.launch_persistent_context(
            str(profile), channel='chrome', headless=False, no_viewport=True,
            ignore_default_args=['--enable-automation', '--no-sandbox'],
            args=['--start-maximized', '--lang=en-US', '--no-first-run', '--no-default-browser-check',
                  '--disable-features=PasswordLeakDetection,Translate'],
        )
        self.page = self.ctx.pages[0] if self.ctx.pages else self.ctx.new_page()
        self.page.set_default_timeout(30000)
        self.hwnd = None

    def window(self):
        if not self.hwnd:
            self.hwnd = find_window('', browser_pids(PROFILE_MARKER))
        return self.hwnd

    def go(self, url, wait=1.2):
        self.page.goto(url, wait_until='networkidle')
        time.sleep(wait)

    def unfocus_omnibox(self):
        # Move keyboard focus from the address bar into the page by clicking an empty spot.
        self.page.mouse.click(3, self.page.evaluate('() => window.innerHeight') - 3)
        self.page.evaluate('() => document.activeElement && document.activeElement.blur()')

    def shot(self, name, wait=0.6, click=True):
        time.sleep(wait)
        path = OUT / f'{name}.png'
        capture_window(self.window(), path, focus_page=click)
        print('saved', path.name, '<-', self.page.url)
        return path

    def scroll_to(self, selector, bottom=None):
        # Scroll `selector` to just below the sticky header; with `bottom`, scroll further only
        # as much as needed to also bring that element fully into view.
        self.page.evaluate("""([s, b]) => {
            const el = document.querySelector(s); if (!el) return;
            let y = el.getBoundingClientRect().top + window.scrollY - 80;
            const end = b && document.querySelector(b);
            if (end) y = Math.max(y, end.getBoundingClientRect().bottom + window.scrollY - window.innerHeight + 24);
            window.scrollTo(0, y);
        }""", [selector, bottom])
        time.sleep(0.8)

    def close(self):
        self.ctx.close()


def fill(page, label, value):
    page.get_by_label(label, exact=True).fill(value)


def run_local(s, base, api):
    p = s.page
    # Make sure we start logged out
    s.go(f'{base}/')
    if p.get_by_role('button', name='Logout').count():
        p.once('dialog', lambda d: d.accept())
        p.get_by_role('button', name='Logout').click()
        time.sleep(1)
    s.unfocus_omnibox()

    s.go(f'{base}/about'); s.scroll_to('.values'); s.shot('task03_about_us')
    s.scroll_to('.team'); s.shot('task03_about_us_team')
    s.go(f'{base}/contact'); s.shot('task04_contact_us')

    s.go(f'{base}/'); s.scroll_to('#dealers'); s.shot('task17_homepage_guest')

    # Sign up (5 fields) — registers the demo user, or logs in if it already exists.
    s.go(f'{base}/register')
    for f, label in [('userName', 'Username'), ('firstName', 'First Name'), ('lastName', 'Last Name'),
                     ('email', 'Email'), ('password', 'Password')]:
        fill(p, label, USER[f])
    s.shot('task07_signup')
    p.get_by_role('button', name='Register').click()
    time.sleep(2)
    if '/register' in p.url:  # already registered -> use the login page instead
        s.go(f'{base}/login')
        fill(p, 'Username', USER['userName']); fill(p, 'Password', USER['password'])
        p.get_by_role('button', name='Login').click()
        p.wait_for_url(f'{base}/')
    time.sleep(1.5)

    s.go(f'{base}/'); s.scroll_to('#dealers', bottom='.card-actions'); s.shot('task18_homepage_loggedin')

    # Logout alert: capture the real browser alert dialog while it is open.
    def on_dialog(dialog):
        s.shot('task06_logout', wait=1.0, click=False)
        dialog.accept()
    p.once('dialog', on_dialog)
    p.get_by_role('button', name='Logout').click()
    time.sleep(2)
    s.shot('task06_logout_confirmation')

    s.go(f'{base}/login')
    fill(p, 'Username', USER['userName']); fill(p, 'Password', USER['password'])
    s.shot('task05_login')
    p.get_by_role('button', name='Login').click()
    p.wait_for_url(f'{base}/')
    time.sleep(1.5)
    s.shot('task05_login_success')

    # Filter by state from the homepage dropdown
    s.go(f'{base}/')
    s.scroll_to('#dealers')
    p.get_by_label('Filter by state').select_option('Kansas')
    p.wait_for_url('**/dealers/Kansas')
    time.sleep(2)
    s.shot('task19_dealers_by_state')

    s.go(f'{base}/dealer/1', wait=2); s.scroll_to('.dealer-hero'); s.shot('task20_dealer_details_reviews')

    s.go(f'{base}/postreview/1', wait=2)
    p.get_by_placeholder('Tell other buyers about your experience…').fill(REVIEW_TEXT)
    p.get_by_role('radio').nth(4).click()
    p.locator('input[type=date]').fill((date.today() - timedelta(days=12)).isoformat())
    p.locator('select').select_option(label='Toyota Camry (2025)')
    p.get_by_role('heading', name='Post a review').click()
    s.shot('task21_review_submission')
    p.get_by_role('button', name='Post Review').click()
    p.wait_for_url(f'{base}/dealer/1')
    time.sleep(2.5)
    s.scroll_to('.review-new')
    s.shot('task22_added_review')

    # Express + MongoDB endpoints
    s.go(f'{api}/fetchReviews/dealer/1'); s.shot('task08_dealer_reviews')
    s.go(f'{api}/fetchDealers'); s.shot('task09_all_dealers')
    s.go(f'{api}/fetchDealer/3'); s.shot('task10_dealer_details_api')
    s.go(f'{api}/fetchDealers/Kansas'); s.shot('task11_kansas_dealers')
    s.go(f'{api}/analyze/Fantastic services'); s.shot('task16_sentiment_analyzer_local')

    # Django admin
    run_admin(s, base)
    s.go(f'{base}/djangoapp/get_cars'); s.shot('task14_car_makes_api')


def run_admin(s, base, suffix=''):
    p = s.page
    s.go(f'{base}/admin/login/?next=/admin/')
    p.locator('#id_username').fill(ADMIN[0])
    p.locator('#id_password').fill(ADMIN[1])
    p.locator('input[type=submit]').click()
    p.wait_for_url(f'{base}/admin/')
    time.sleep(1)
    s.shot(f'task12_admin_login{suffix}')
    s.go(f'{base}/admin/djangoapp/carmake/'); s.shot(f'task14_car_makes{suffix}')
    s.go(f'{base}/admin/djangoapp/carmodel/'); s.shot(f'task15_car_models{suffix}')
    p.locator('#logout-form button, #logout-form input[type=submit]').first.click()
    time.sleep(1.5)
    s.shot(f'task13_admin_logout{suffix}')


def run_deployed(s, base, api):
    p = s.page
    s.go(f'{base}/', wait=3); s.shot('task25_deployed_landingpage')
    s.go(f'{base}/login')
    fill(p, 'Username', USER['userName']); fill(p, 'Password', USER['password'])
    p.get_by_role('button', name='Login').click()
    time.sleep(3)
    if '/login' in p.url:  # first visit: register the demo user on the deployed site
        s.go(f'{base}/register')
        for f, label in [('userName', 'Username'), ('firstName', 'First Name'), ('lastName', 'Last Name'),
                         ('email', 'Email'), ('password', 'Password')]:
            fill(p, label, USER[f])
        p.get_by_role('button', name='Register').click()
        time.sleep(3)
    s.go(f'{base}/', wait=2); s.scroll_to('#dealers', bottom='.card-actions'); s.shot('task26_deployed_loggedin')
    s.go(f'{base}/dealer/3', wait=3); s.scroll_to('.dealer-hero'); s.shot('task27_deployed_dealer_detail')
    s.go(f'{base}/postreview/3', wait=2)
    p.get_by_placeholder('Tell other buyers about your experience…').fill(
        'Deployed test: fantastic services and a very helpful, friendly team.')
    p.get_by_role('radio').nth(4).click()
    p.locator('input[type=date]').fill((date.today() - timedelta(days=5)).isoformat())
    p.locator('select').select_option(label='BMW X5 (2026)')
    p.get_by_role('heading', name='Post a review').click()
    p.get_by_role('button', name='Post Review').click()
    p.wait_for_url(f'{base}/dealer/3')
    time.sleep(3)
    s.scroll_to('.review-new')
    s.shot('task28_deployed_add_review')
    s.go(f'{api}/analyze/Fantastic services', wait=2); s.shot('task16_sentiment_analyzer')


def run_github(s, repo):
    s.go(f'https://github.com/{repo}/actions', wait=3); s.shot('task23_github_actions_list')
    s.page.locator('a[href*="/actions/runs/"]').first.click()
    s.page.wait_for_load_state('networkidle')
    s.shot('task23_github_actions', wait=2.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['local', 'admin', 'deployed', 'github'])
    parser.add_argument('--base', default='http://localhost:8000')
    parser.add_argument('--api', default='http://localhost:3030')
    parser.add_argument('--repo', default='jsowkw1/Django-React-Car-Dealership-Capstone')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        s = Shooter(pw)
        try:
            if args.stage == 'local':
                run_local(s, args.base.rstrip('/'), args.api.rstrip('/'))
            elif args.stage == 'admin':
                run_admin(s, args.base.rstrip('/'))
            elif args.stage == 'deployed':
                run_deployed(s, args.base.rstrip('/'), args.api.rstrip('/'))
            else:
                run_github(s, args.repo)
        finally:
            s.close()


if __name__ == '__main__':
    main()
