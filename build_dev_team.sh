#!/bin/sh

set -e # stops execution on error
rm -rf server/api/migrations
python server/manage.py schemamigration api --initial
python server/manage.py syncdb --noinput
python server/manage.py migrate api
python server/manage.py test
