import importlib

from wsgi_framework.config import APPS, AppModules
from wsgi_framework.creational_patterns.singleton import SingletonMeta


class RouterSingleton(dict, metaclass=SingletonMeta):
    pass


def prettiry_url(url: str):
    url = url if not url or url.endswith("/") else f"{url}/"
    url = url if not url or url.startswith("/") else f"/{url}"
    return url


main_router = RouterSingleton()

for app in APPS:
    try:
        router_module: dict = importlib.import_module(f"{app}.{AppModules.router}")
        for path, view in router_module.routes.items():
            # TODO: check is callable, cast type to object
            main_router[prettiry_url(path)] = view
    except ImportError:
        pass
