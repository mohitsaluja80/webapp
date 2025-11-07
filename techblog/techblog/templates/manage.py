#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create PostgreSQL database if it doesn't exist."""
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    try:
        conn = psycopg2.connect(dbname="postgres", user=db_user, password=db_password, host=db_host, port=db_port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

# Call the function before running the Django app
create_database()


import django
from django.core.management import execute_from_command_line

def apply_migrations():
    """Apply migrations automatically."""
    try:
        execute_from_command_line(["manage.py", "migrate"])
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")

apply_migrations()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techblog.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



# #!/bin/bash
# set -e

# echo "Waiting for PostgreSQL to start..."
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
#   sleep 1
# done

# echo "Applying database migrations..."
# python manage.py migrate

# exec "$@"