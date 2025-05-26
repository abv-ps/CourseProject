#!/bin/bash

export PGPASSWORD=$FASTAPI_POSTGRES_PASSWORD

until psql -h postgres-fastapi -p 5432 -U bur -d booksdb -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

alembic -c alembic.ini upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
