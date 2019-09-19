#!/bin/bash
PGPASSWORD=$DB_PASSWORD dropdb helios --host=$DB_HOST --username=$DB_USER
PGPASSWORD=$DB_PASSWORD createdb helios --host=$DB_HOST --username=$DB_USER
python manage.py syncdb --noinput
python manage.py migrate

# Create a superuser
echo "from helios_auth.models import User; User.objects.create(\
  user_type='password',\
  user_id='admin',\
  name='Admin',\
  admin_p='true', \
  info={'name':'Admin', 'password':'admin'})" | python manage.py shell
