#!/bin/sh
set -e

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

: "${UWSGI_PROCESSES:=2}"
: "${UWSGI_THREADS:=2}"
: "${UWSGI_HARAKIRI:=60}"
export UWSGI_PROCESSES UWSGI_THREADS UWSGI_HARAKIRI

mkdir -p /opt/app/static /var/www/static /var/www/media
chown -R app:app /opt/app/static /var/www/static /var/www/media

if [ "$(id -u)" = "0" ]; then
    su -s /bin/sh app -c "python manage.py shell <<'PY'
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('CREATE SCHEMA IF NOT EXISTS content;')
PY"
    su -s /bin/sh app -c "python manage.py migrate --noinput"
    su -s /bin/sh app -c "python manage.py collectstatic --noinput"
    su -s /bin/sh app -c "python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '1234')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

User = get_user_model()
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f\"Superuser '{username}' created\")
else:
    print(f\"Superuser '{username}' already exists\")
PY"
    exec su -s /bin/sh app -c "uwsgi --strict --ini /opt/app/uwsgi.ini"
fi

python manage.py shell <<'PY'
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('CREATE SCHEMA IF NOT EXISTS content;')
PY
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '1234')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

User = get_user_model()
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created")
else:
    print(f"Superuser '{username}' already exists")
PY
exec uwsgi --strict --ini /opt/app/uwsgi.ini
