#!/bin/bash

# start django
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate --run-syncdb
#python manage.py test vsc
#python manage.py runserver
gunicorn djangoproject.wsgi -b 0.0.0.0:8000
