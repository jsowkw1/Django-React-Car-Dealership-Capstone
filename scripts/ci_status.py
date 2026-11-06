"""Prints the latest GitHub Actions run of this repository with every job and step (public GitHub API).

    python scripts/ci_status.py [owner/repo]
"""
import json
import sys
import urllib.request

REPO = sys.argv[1] if len(sys.argv) > 1 else 'jsowkw1/Django-React-Car-Dealership-Capstone'
API = f'https://api.github.com/repos/{REPO}'


def get(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'ci-status'})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


run = get(f'{API}/actions/runs?per_page=1&branch=main')['workflow_runs'][0]
print(f"Workflow : {run['name']} (.github/workflows/ci.yml)")
print(f"Run      : #{run['run_number']}  {run['html_url']}")
print(f"Commit   : {run['head_sha'][:7]}  {run['display_title']}")
print(f"Trigger  : {run['event']} on {run['head_branch']} by {run['actor']['login']}")
print(f"Started  : {run['run_started_at']}   Updated: {run['updated_at']}")
print(f"Status   : {run['status']}  Conclusion: {run['conclusion']}")
print()
for job in get(run['jobs_url'])['jobs']:
    print(f"JOB  {job['name']}  ->  {job['conclusion']}")
    for step in job['steps']:
        mark = '✓' if step['conclusion'] == 'success' else ('-' if step['conclusion'] == 'skipped' else '✗')
        print(f"     {mark} {step['number']:>2}. {step['name']}  [{step['conclusion']}]")
    print()
