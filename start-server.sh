#!/usr/bin/env bash
set -e  # Exit immediately if any command fails

echo "Starting the Django application setup..."

# Wait for PostgreSQL to be ready
echo "Waiting for database..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done
echo "Database is ready."

# Connect to PostgreSQL and create the database if it does not exist
echo "Checking and creating database if needed..."
export PGPASSWORD="$PGUSER_PASSWORD"
psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
psql -U postgres -h "$DB_HOST" -p "$DB_PORT" -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
echo "[✔] Database setup completed."

# Ensure correct database permissions
echo "Setting up database permissions..."
psql -U postgres -h "$DB_HOST" -p "$DB_PORT" <<EOSQL
    ALTER DATABASE $DB_NAME OWNER TO $DB_USER;
    ALTER SCHEMA public OWNER TO $DB_USER;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    GRANT USAGE, CREATE ON SCHEMA public TO $DB_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
EOSQL
echo "[✔] Database permissions ensured."

# Apply Django migrations
echo "Applying migrations..."
cd techblog
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
echo "[✔] Migrations and static files collected."

# Create a superuser if not exists
echo "Ensuring superuser exists..."
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
    print("[✔] Superuser created successfully.")
else:
    print("[✔] Superuser already exists.")
EOF

# Ensure Features table has an entry
echo "Checking Features table..."
python3 manage.py shell <<EOF
from web.models import Features

if not Features.objects.exists():
    Features.objects.create(
        color_schem="blue",
        onfocus=True,
        testimonials=True,
        pricing=False,
        portfolio=True,
        faq=False,
        team=False,
        recentblogs=True,
        services=True,
        about=True,
        contact=True
    )
    print("[✔] Features table initialized with default entry.")
else:
    print("[✔] Features table already has an entry.")
EOF

# Start Gunicorn and Nginx
echo "Starting Gunicorn..."
exec gunicorn techblog.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 &

echo "Starting Nginx..."
exec nginx -g "daemon off;"