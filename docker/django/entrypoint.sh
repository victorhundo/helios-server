#!/bin/bash

cd /app

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\l'  2> /dev/null; do
    sleep 1
done

if [ -z "$API" ]; then
  pip install -r requirements.txt
  ./reset.sh
  python manage.py compilemessages
  python manage.py runserver 0.0.0.0:8000
else
  pip install -r api-requirements.txt
  PGPASSWORD=$DB_PASSWORD dropdb helios --host=$DB_HOST --username=$DB_USER
  PGPASSWORD=$DB_PASSWORD createdb helios --host=$DB_HOST --username=$DB_USER
  python api.py migrate
  python api.py runserver 0.0.0.0:8000
fi

tail -f /dev/null
