#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
try:
    import dotenv
except ImportError:
    pass

import pathlib


def main():
    """Run administrative tasks."""
    DOT_ENV_PATH = pathlib.Path() / '.env'
    if DOT_ENV_PATH.exists():
        dotenv.load_dotenv(str(DOT_ENV_PATH))
    # dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogWebApp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if the command is `runserver`
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        port = os.getenv("PORT",8000)  # Default port is 8000 if PORT is not set
        sys.argv = ["manage.py", "runserver", f"0.0.0.0:{port}"]

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()