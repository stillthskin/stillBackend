#!/bin/bash
set -e

# Wait for DB if you want (optional)
# until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT; do sleep 1; done

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn myproject.wsgi:application -w 3 -b 0.0.0.0:8000
