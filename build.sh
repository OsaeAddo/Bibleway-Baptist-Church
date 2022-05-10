#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
poetry install

# python manage.py collectstatic --no-input
python prod-manage.py makemigrations
python prod-manage.py migrate