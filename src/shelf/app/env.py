"""Environment variable access layer.

Provides configuration values loaded from
OS environment variables.
"""

import os

POSTGRES_USER = os.environ.get('POSTGRES_USER', 'shelf_user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'shelf')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'shelf_db')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
