#!/bin/bash

cd /app

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\l'  2> /dev/null; do
    sleep 1
done

pip install -r api-requirements.txt
python api.py migrate
python api.py runserver 0.0.0.0:8000

tail -f /dev/null
