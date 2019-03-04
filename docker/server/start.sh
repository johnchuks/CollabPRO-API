#!/bin/bash
set -e
set -o pipefail # if any code doesn't return 0, exit the script

function run_migration() {
  python manage.py makemigrations
  python manage.py migrate
}

run_migration
# Start Gunicorn server
echo Starting Gunicorn.
exec gunicorn dev_team_app.wsgi:application \
    --bind 0.0.0.0:9000 \
    --workers 3

exit 0
