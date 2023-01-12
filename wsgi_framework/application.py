class Application:
    def __init__(self, routes: dict, fronts: list):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        path = path if path.endswith("/") else f"{path}/"
        try:
            view = self.routes.get(path) or self.routes[None]
        except KeyError:
            raise TypeError("Нужно определить маршрут 'None' со представлением по умолчанию для ошибки 404")
        request = {}
        for front in self.fronts:
            front(request)
        code, body_text = view(request)
        body = [body_text.encode()]

        start_response(code, [("Content-Type", "text/html")])
        return body
