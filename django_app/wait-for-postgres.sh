#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$DJANGO_POSTGRES_PASSWORD psql -h "$host" -U "$DJANGO_POSTGRES_USER" -d "$DJANGO_POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - executing command"
exec $@
