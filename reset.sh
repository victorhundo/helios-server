#!/bin/bash
PGPASSWORD=$DB_PASSWORD dropdb helios --host=$DB_HOST --username=$DB_USER
PGPASSWORD=$DB_PASSWORD createdb helios --host=$DB_HOST --username=$DB_USER
python manage.py syncdb --noinput
python manage.py migrate

# Create a admin user
echo "from helios_auth.models import User; User.update_or_create(\
  'password',\
  'admin',\
  'Admin',\
  {'name':'Admin', 'password':'admin'}\
  )"| python manage.py shell
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d"helios" -c "update helios_auth_user set admin_p='t' where user_id='admin'";
