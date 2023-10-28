#!/bin/bash

python ./manage.py collectstatic --noinput
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py generate_100_recipes
gunicorn config.wsgi:application --bind 0.0.0.0:8000