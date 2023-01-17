import importlib
from inspect import getmembers, isfunction

import wsgi_framework.builtin_middleware as builtin_middleware_module
from wsgi_framework.config import APPS, MIDDLEWARE, AppModules

builtin_middleware = dict(getmembers(builtin_middleware_module, isfunction))
applied_middleware = dict(filter(lambda x: x[0] in MIDDLEWARE, builtin_middleware.items()))

for app in APPS:
    try:
        app_middleware_module = importlib.import_module(f"{app}.{AppModules.front_controller}")
    except ImportError:
        pass
    else:
        app_middleware = dict(getmembers(app_middleware_module, isfunction))
        for mw_name, mw_fnc in app_middleware.items():
            if mw_name in MIDDLEWARE:
                applied_middleware.update(app_middleware)

applied_middleware = applied_middleware.values()
