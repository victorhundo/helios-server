#!/bin/bash
PGPASSWORD=$DB_PASSWORD dropdb helios --host=$DB_USER --username=$DB_USER
PGPASSWORD=$DB_PASSWORD createdb helios --host=$DB_USER --username=$DB_USER
python manage.py syncdb --noinput
python manage.py migrate

# Create a superuser
echo "from helios_auth.models import User; User.objects.create(user_type='google',user_id='vhfsfox@gmail.com', info={'name':'Victor Hugo'})" | python manage.py shell
