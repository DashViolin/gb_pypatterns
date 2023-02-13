from quopri import decodestring


class RequestParser:
    query_data_tag = "query"
    post_data_tag = "data"

    def _decode_param(self, value: str) -> str:
        bytes_val = bytes(value.replace("%", "=").replace("+", " "), "UTF-8")
        return decodestring(bytes_val).decode("UTF-8")

    def _parse_params(self, params: dict) -> dict:
        if params:
            return {
                key: self._decode_param(value) for key, value in map(lambda item: item.split("="), params.split("&"))
            }
        return {}

    def _parse_query_params(self, environ: dict) -> dict:
        query_string = environ.get("QUERY_STRING")
        return self._parse_params(query_string)

    def _parse_data_params(self, environ: dict) -> dict:
        content_length_data = environ.get("CONTENT_LENGTH")
        content_length = int(content_length_data) if content_length_data else 0
        data = environ["wsgi.input"].read(content_length) if content_length > 0 else b""
        params_str = data.decode(encoding="UTF-8")
        return self._parse_params(params_str)

    def parse_query_params(self, environ: dict, request: dict) -> None:
        request[self.query_data_tag] = self._parse_query_params(environ)

    def parse_post_params(self, environ: dict, request: dict) -> None:
        self.parse_query_params(environ, request)
        request[self.post_data_tag] = self._parse_data_params(environ)

    @staticmethod
    def print_params(request: dict) -> None:
        params_dict = request.copy()
        method = params_dict.pop("method")
        params_str = ", ".join(f"{key}={value}" for key, value in params_dict.items())
        info = f"\n[METHOD: {method}] - PARAMS: {params_str}\n"
        print(info)
