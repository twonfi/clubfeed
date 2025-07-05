#!/usr/bin/env bash
# Used by Render build
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
