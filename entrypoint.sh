#!/bin/bash

echo "Waiting for PostgreSQL DB ..."

export PGPASSWORD=${POSTGRES_PASSWORD}

until psql -h postgres-db -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing database setup commands"

python -m app.models
python -m examples.content
python -m examples.ratings

exec "$@"