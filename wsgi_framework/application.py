class Application:
    def __init__(self, routes: dict, fronts: list):
        self.routes = routes
        self.fronts = fronts

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
        match method:
            case "GET":
                query_string = environ["QUERY_STRING"]
                if query_string:
                    self.__parse_params(query_string, request)
                    self.__print_params(method, request)
            case "POST":
                content_length_data = environ.get("CONTENT_LENGTH")
                content_length = int(content_length_data) if content_length_data else 0
                data = environ["wsgi.input"].read(content_length) if content_length > 0 else b""
                if data:
                    params_str = data.decode(encoding="utf-8")
                    self.__parse_params(params_str, request)
                    self.__print_params(method, request)
            case _:
                pass

        for front in self.fronts:
            front(request)

        code, body_text = view(request)
        body = [body_text.encode()]
        start_response(code, [("Content-Type", "text/html")])
        return body

    def __parse_params(self, query: str, request: dict):
        if query:
            params = {key: value for key, value in map(lambda item: item.split("="), query.split("&"))}
            request.update(params)

    def __print_params(self, method: str, params: dict):
        params_str = ", ".join(f"{key} = {value}" for key, value in params.items())
        info = f"\nMETHOD: {method}\nPARAMS: {params_str}\n"
        print(info)
