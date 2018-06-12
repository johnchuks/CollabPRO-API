#!/bin/sh

set -e # stops execution on error
python server/manage.py makemigrations
python server/manage.py migrate
python server/manage.py test api
