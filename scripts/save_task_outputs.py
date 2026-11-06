"""Runs the cURL commands the peer-graded form asks for and saves each command + its REAL output
in submission/outputs/<required file name> (loginuser, logoutuser, getdealerreviews, ...).

    python scripts/save_task_outputs.py [--deployed https://<app>.onrender.com]
Requires curl, the Express API on :3030 and Django on :8000.
"""
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'submission' / 'outputs'
API = 'http://localhost:3030'
WEB = 'http://localhost:8000'
USER = os.getenv('DEMO_USERNAME', 'jsowkw1')
PASSWORD = os.getenv('DEMO_PASSWORD', 'DriveSafe#2026')
JAR = Path(tempfile.gettempdir()) / 'cookies.txt'


def curl(args):
    return subprocess.run(['curl', '-s'] + args, capture_output=True, text=True, encoding='utf-8').stdout


def pretty(body):
    try:
        return json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except ValueError:
        return body


def csrf():
    for line in JAR.read_text().splitlines():
        parts = line.split('\t')
        if len(parts) == 7 and parts[5] == 'csrftoken':
            return parts[6]
    return ''


def save(name, blocks):
    text = '\n\n'.join(f'$ {cmd}\n{out}' for cmd, out in blocks).strip() + '\n'
    (OUT / name).write_text(text, encoding='utf-8')
    print('saved', name)


def simple(name, url):
    save(name, [(f'curl -s "{url}"', pretty(curl([url])))])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployed', default='https://bestcars-dealership-i2j9.onrender.com')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    JAR.unlink(missing_ok=True)

    # Login / logout through Django: get the CSRF cookie first, then POST with the X-CSRFToken header.
    get_cookie = f'curl -s -c cookies.txt {WEB}/djangoapp/me'
    me = curl(['-c', str(JAR), f'{WEB}/djangoapp/me'])
    body = json.dumps({'userName': USER, 'password': PASSWORD})
    login_args = ['-b', str(JAR), '-c', str(JAR), '-X', 'POST', f'{WEB}/djangoapp/login',
                  '-H', 'Content-Type: application/json', '-H', f'X-CSRFToken: {csrf()}', '-d', body]
    login_cmd = (f'curl -s -b cookies.txt -c cookies.txt -X POST {WEB}/djangoapp/login '
                 f'-H "Content-Type: application/json" -H "X-CSRFToken: <csrftoken from cookies.txt>" '
                 f"-d '{body}'")
    login_out = curl(login_args)
    save('loginuser', [(get_cookie, pretty(me)), (login_cmd, pretty(login_out))])

    logout_cmd = (f'curl -s -b cookies.txt -c cookies.txt -X POST {WEB}/djangoapp/logout '
                  f'-H "X-CSRFToken: <csrftoken from cookies.txt>"')
    logout_out = curl(['-b', str(JAR), '-c', str(JAR), '-X', 'POST', f'{WEB}/djangoapp/logout',
                       '-H', f'X-CSRFToken: {csrf()}'])
    save('logoutuser', [(logout_cmd, pretty(logout_out))])
    JAR.unlink(missing_ok=True)

    simple('getdealerreviews', f'{API}/fetchReviews/dealer/1')
    simple('getalldealers', f'{API}/fetchDealers')
    simple('getdealerbyid', f'{API}/fetchDealer/3')
    simple('getdealersbyState', f'{API}/fetchDealers/Kansas')
    simple('getallcarmakes', f'{WEB}/djangoapp/get_cars')
    simple('analyzereview', f'{args.deployed}/djangoapp/analyze/Fantastic%20services')
    (OUT / 'deploymentURL').write_text(args.deployed + '\n', encoding='utf-8')
    print('saved deploymentURL')


if __name__ == '__main__':
    main()
