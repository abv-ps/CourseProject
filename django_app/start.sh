#!/bin/bash

./wait-for-postgres.sh custom_postgres

python manage.py makemigrations
python manage.py migrate
uvicorn my_site.asgi:application --host 0.0.0.0 --port 8000 --reload
