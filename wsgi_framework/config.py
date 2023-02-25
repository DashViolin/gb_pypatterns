import os

from settings import *

try:
    DEBUG_MODE = DEBUG_MODE
except NameError:
    DEBUG_MODE = False

try:
    BASE_TEMPLATES_PATH = BASE_TEMPLATES_PATH
except NameError:
    BASE_TEMPLATES_PATH = BASE_DIR / "templates"

try:
    BASE_STATIC_PATH = BASE_STATIC_PATH
except NameError:
    BASE_STATIC_PATH = BASE_DIR / "static"

try:
    MIDDLEWARE = MIDDLEWARE
except NameError:
    MIDDLEWARE = []

try:
    SQLITE_DB_PATH = SQLITE_DB_PATH
except NameError:
    SQLITE_DB_PATH = BASE_DIR / "data" / "py_patterns.sqlite"

try:
    SQLITE_DB_INIT_SCRIPT_PATH = SQLITE_DB_INIT_SCRIPT_PATH
except NameError:
    SQLITE_DB_INIT_SCRIPT_PATH = BASE_DIR / "wsgi_framework" / "architectural_system_patterns" / "create_db.sql"


for path in [SQLITE_DB_PATH.parent, BASE_TEMPLATES_PATH, BASE_STATIC_PATH]:
    if not path.exists():
        os.makedirs(path, exist_ok=True)


class ServerConf:
    port = 8000


class AppModules:
    front_controller = "middleware"
    router = "router"
