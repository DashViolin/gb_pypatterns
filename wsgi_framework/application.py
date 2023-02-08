from wsgi_framework.requests_parser import RequestParser


class Application:
    def __init__(self, routes: dict, fronts: list, debug_mode: bool = False):
        self.routes = routes
        self.fronts = fronts
        self.request_parser = RequestParser()
        self.debug_mode = debug_mode

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        endpoint = environ["PATH_INFO"]
        endpoint = endpoint if endpoint.endswith("/") else f"{endpoint}/"
        try:
            view = self.routes.get(endpoint) or self.routes[None]
        except KeyError:
            raise TypeError("Нужно определить маршрут None с представлением по умолчанию для обработки ошибки 404")
        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method
        # TODO: refactor that
        match method:
            case "GET":
                self.request_parser.parse_get_params(environ, request)
            case "POST":
                self.request_parser.parse_post_params(environ, request)
            case _:
                pass

        for front in self.fronts:
            front(request)

        if self.debug_mode:
            self.request_parser.print_params(request)

        code, body_text = view(request)
        body = [body_text.encode()]
        start_response(code, [("Content-Type", "text/html")])
        return body


class FakeApplication(Application):
    def __init__(self, routes: dict, fronts: list):
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"Hello from Fake Application"]
