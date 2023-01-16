import importlib

from wsgi_framework.config import APPS, AppModules

main_router = dict()

for app in APPS:
    router_module: dict = importlib.import_module(f"{app}.{AppModules.router}")
    for path, view in router_module.routes.items():
        main_router.update({path if not path or path.endswith("/") else f"{path}/": view})
