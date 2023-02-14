import importlib
from inspect import isclass

from wsgi_framework.config import APPS, AppModules
from wsgi_framework.creational_patterns.singleton import SingletonMeta


class RouterSingleton(dict, metaclass=SingletonMeta):
    pass


def prettify_url(url: str):
    url = url if not url or url.endswith("/") else f"{url}/"
    url = url if not url or url.startswith("/") else f"/{url}"
    return url


main_router = RouterSingleton()

for app in APPS:
    try:
        router_module = importlib.import_module(f"{app}.{AppModules.router}")
        routes: dict = router_module.routes
        for path, view in routes.items():
            if not callable(view):
                raise TypeError(f'View "{view.__name__}" is not callable object.')
            path = prettify_url(path)
            if path in main_router:
                raise KeyError(f'Route registration conflict: remove endpoint "{path}" from app router.')
            main_router[path] = view() if isclass(view) else view
    except ImportError:
        pass
