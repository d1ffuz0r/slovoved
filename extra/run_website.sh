#!/usr/bin/env bash

NAME="slovoved"                                # Name of the application
DJANGODIR=/var/www/slovoved/                   # Django project directory
SOCKFILE=/tmp/gunicorn_slovoved.sock           # we will communicate using this unix socket
USER=cyberkolhoz                               # the user to run as
GROUP=cyberkolhoz                              # the group to run as
NUM_WORKERS=1                                  # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=slovoved.settings_prod  # which settings file should Django use
DJANGO_WSGI_MODULE=slovoved.wsgi               # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ./venv/bin/activate

export PYTHONPATH=slovoved
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=INFO \
  --log-file=-
