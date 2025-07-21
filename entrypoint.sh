#!/bin/bash

echo "Waiting for PostgreSQL DB ..."

export PGPASSWORD=${POSTGRES_PASSWORD}

until psql -h postgres-db -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing database setup commands if empty"

TABLE_COUNT=$(psql -h postgres-db -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB} -t -A -q -c "SELECT count(*) FROM pg_tables WHERE schemaname = 'public';" 2>/dev/null)

unset PGPASSWORD

if [[ -z "$TABLE_COUNT" ]]; then
  echo "Error: Could not connect to the database or query for tables. Proceding anyway"
elif (( TABLE_COUNT == 0 )); then
  echo "Database '${DB_NAME}' is empty. Running data initialization"
  alembic upgrade head
  python -m examples.fake_content
else
  echo "Database '${DB_NAME}' already has ${TABLE_COUNT} relations. Skipping initialization."
fi

exec "$@"