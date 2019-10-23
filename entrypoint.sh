#!/bin/bash
python manage.py db upgrade
gunicorn -b 0.0.0.0:5001 --workers 20 app:app