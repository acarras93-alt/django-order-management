#!/usr/bin/env python
"""
Django command-line utility for administrative tasks.

Backend responsibility:
- Load the Django project settings.
- Expose management commands such as runserver, migrate, makemigrations,
createsuperuser and shell.
- Act as the entry point for local development and project administration.
"""

import os
import sys


def main():
    """
    Run Django administrative tasks from the command line.

    This function configures the settings module and delegates command
    execution to Django's management system.
    """

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "proyecto_web_inicial.settings",
    )

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()