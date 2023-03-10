import pathlib

DEBUG_MODE = True

BASE_DIR = pathlib.Path().resolve()

BASE_TEMPLATES_PATH = BASE_DIR / "templates"
BASE_STATIC_PATH = BASE_DIR / "static"


APPS = [
    "simple_site_app",
]

APP_TEMPLATES_DIR_NAME = "templates"

MIDDLEWARE = [
    "secret_front",
    "other_front",
    "date_middleware",
]

SQLITE_DB_PATH = BASE_DIR / "data" / "py_patterns.sqlite"
SQLITE_DB_INIT_SCRIPT_PATH = BASE_DIR / "data" / "create_db.sql"
