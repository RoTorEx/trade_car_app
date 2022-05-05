#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started!"
fi

# Remove old Celery logs
rm celerybeat-schedule && rm data/celery.log

# Flush DB
python manage.py flush --no-input

# Fill DB
python manage.py fill_db

exec "$@"
