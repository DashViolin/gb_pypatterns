from settings import *

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


class ServerConf:
    port = 8000


class AppModules:
    front_controller = "middleware"
    router = "router"
