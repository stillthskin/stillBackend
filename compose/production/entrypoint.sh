#!/bin/bash
set -e

echo "🚀 Starting Django container..."

# Optional: Wait for DB only if DATABASE_HOST is defined (Postgres/MySQL)
if [ -n "$DATABASE_HOST" ]; then
  echo "⏳ Waiting for database at $DATABASE_HOST..."
  until nc -z "$DATABASE_HOST" "${DATABASE_PORT:-5432}"; do
    echo "Database not ready yet... sleeping 1s"
    sleep 1
  done
  echo "✅ Database is up!"
else
  echo "⚙️  Using SQLite (no DB wait needed)"
fi

# Run migrations & collectstatic safely
echo "⚙️  Applying migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "🚀 Launching Gunicorn server..."
exec gunicorn myproject.wsgi:application -w 3 -b 0.0.0.0:8000


