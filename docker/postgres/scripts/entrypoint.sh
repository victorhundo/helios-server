#!/bin/bash

psql -c "create role helios with createdb createrole login;"
psql -c "alter user helios with password 'mudar123';"

echo "local all helios md5" >> /var/lib/postgresql/data/pg_hba.conf
