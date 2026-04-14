#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Fixing Python 3.12 compatibility..."
pip install --upgrade pip setuptools

echo "Installing dependencies..."
pip install -r requirements.txt

# Force install deployment packages
pip install gunicorn whitenoise python-dotenv

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files for production..."
python manage.py collectstatic --no-input
