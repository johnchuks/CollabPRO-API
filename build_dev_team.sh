#!/bin/sh

set -e # stops execution on error
python server/manage.py syncdb --noinput
python server/manage.py test
