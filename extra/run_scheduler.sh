#!/usr/bin/env bash

NAME="slovoved"
DJANGODIR=/var/www/slovoved/                       # Django project directory
DJANGO_SETTINGS_MODULE=slovoved.settings_prod      # which settings file should Django use

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../../venv/bin/activate
source .env

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=slovoed
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec celery beat \
    -A slovoved \
    -l INFO
