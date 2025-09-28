#!/bin/bash

echo "Waiting for PostgreSQL DB ..."

# Set variable for password to access the database
export PGPASSWORD=${POSTGRES_PASSWORD}

# Loop until the DB can get a connection
until psql -h backend-db -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing database setup commands if empty"

# Execute a SQL Query to know if there is data in the database
TABLE_COUNT=$(psql -h backend-db -p 5432 -U ${POSTGRES_USER} -d ${POSTGRES_DB}\
              -t -A -q -c "SELECT count(*) FROM pg_tables WHERE schemaname = 'public';"\
               2>/dev/null)

# Clean the password variables
unset PGPASSWORD


if [[ -z "$TABLE_COUNT" ]]; then
  echo "Error: Could not connect to the database or query for tables. Proceding anyway"
# If there are no tables, then use alembic to get teh schemas and example.fake_content to create fake content
elif (( TABLE_COUNT == 0 )); then
  echo "Database '${DB_NAME}' is empty. Running data initialization"
  alembic upgrade head
  python -m generator.init_content_db
# If it already has information don't do anything
else
  echo "Database '${DB_NAME}' already has ${TABLE_COUNT} relations. Skipping initialization."
fi

# Return to the execution of the command in the Dockerfile
exec "$@"