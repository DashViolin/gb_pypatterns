def some_middleware(request: dict):
    request.update({"my_middleware_key": "My middleware param"})
