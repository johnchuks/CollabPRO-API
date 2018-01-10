#!/bin/sh

set -e # stops execution on error
rm -rf server/api/migrations
python manage.py schemamigration api --initial
python manage.py syncdb --noinput
python manage.py migrate api
python manage.py test
