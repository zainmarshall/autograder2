#!/bin/bash

# Wait for PostgreSQL to be ready
until (PGPASSWORD=postgres psql -h "db" -U "postgres" -c '\q') 2> /dev/null; do
  >&2 echo "waiting for postgres"
  sleep 1
done

# Install dependencies
uv sync

uv run manage.py collectstatic --noinput
# Run migrations
uv run manage.py makemigrations --noinput
uv run manage.py migrate
# go create superuser amnually because the command is broken and I changed it like 5 times
# Run server in a loop
while true
do
    uv run uvicorn autograder.asgi:application --reload --host 0.0.0.0 --port 3000
    sleep 1
done