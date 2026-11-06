#!/bin/sh
# Container entrypoint: starts the Express API in the background, prepares Django, then runs gunicorn.
set -e

# Shared secret between Django and Express for POST /insert_review
if [ -z "$EXPRESS_API_KEY" ]; then
  EXPRESS_API_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
fi
export EXPRESS_API_KEY

cd /app/server/database
PORT=3030 API_KEY="$EXPRESS_API_KEY" node server.js &

cd /app/server
python manage.py migrate --noinput
python manage.py seed_demo

exec gunicorn djangoproj.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-1}" --threads 4 --timeout 60 \
  --access-logfile -
