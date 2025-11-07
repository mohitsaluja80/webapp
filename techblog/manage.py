#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def create_database():
    """Create PostgreSQL database if it doesn't exist."""
    db_name = os.getenv("DB_NAME")
    db_user = 'postgres'
    db_password = os.getenv("PGUSER_PASSWORD")
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
            print(f"[✔] Database '{db_name}' created successfully.")
        else:
            print(f"[✔] Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

# Call the function before running the Django app

def ensure_db_permissions():
    """Ensure the PostgreSQL user has necessary permissions."""
    try:
        dbname = os.getenv("DB_NAME", "mydatabase")
        user = os.getenv("DB_USER", "myuser")
        password = os.getenv("PGUSER_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        # Connect to PostgreSQL as a superuser
        conn = psycopg2.connect(dbname="postgres", user="postgres", password=password, host=host, port=port)
        conn.autocommit = True
        cur = conn.cursor()

        # Grant permissions if not already granted
        cur.execute(f"""
            ALTER DATABASE {dbname} OWNER TO {user};
            ALTER SCHEMA public OWNER TO {user};
            GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {user};
            GRANT USAGE, CREATE ON SCHEMA public TO {user};
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {user};
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {user};
        """)
        cur.close()
        conn.close()
        print("[✔] Database permissions ensured.")

    except Exception as e:
        print(f"[✘] Failed to ensure DB permissions: {e}")

def apply_migrations():
    """Apply migrations automatically."""
    try:
        execute_from_command_line(["manage.py", "migrate"])
        print("[✔] Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")


def create_superuser():
    """Automatically create a Django superuser if it doesn't exist."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techblog.settings")
    django.setup()
    
    User = get_user_model()
    admin_username = os.getenv("DJANGO_ADMIN_USER", "admin")
    admin_email = os.getenv("DJANGO_ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("DJANGO_ADMIN_PASSWORD", "admin123")

    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
        print(f"[✔] Superuser '{admin_username}' created successfully.")
    else:
        print(f"[✔] Superuser '{admin_username}' already exists.")


def ensure_features_entry():
    """Ensure there is exactly one entry in the Features table."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techblog.settings")
    django.setup()
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
    create_database()
    ensure_db_permissions()
    apply_migrations()
    create_superuser()
    ensure_features_entry()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
   main()
