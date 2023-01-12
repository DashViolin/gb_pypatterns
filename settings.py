import pathlib

BASE_DIR = pathlib.Path().resolve()

TEMPLATES_DIR = BASE_DIR / "templates"


APPS = [
    "simple_site_app",
]


MIDDLEWARE = [
    "secret_front",
    "other_front",
    "some_middleware",
]
