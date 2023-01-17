from wsgiref.simple_server import make_server

from wsgi_framework.application import Application
from wsgi_framework.config import ServerConf
from wsgi_framework.front_controller import applied_middleware
from wsgi_framework.router import main_router


def startserver(port: int | str = ServerConf.port):
    application = Application(routes=main_router, fronts=applied_middleware)
    port = int(port) or ServerConf.port

    with make_server("", port, application) as http_server:
        print(f"Serving on port {port}...")
        http_server.serve_forever()
