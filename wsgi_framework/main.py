from wsgiref.simple_server import make_server

from wsgi_framework.application import Application, FakeApplication
from wsgi_framework.config import DEBUG_MODE, ServerConf
from wsgi_framework.front_controller import applied_middleware
from wsgi_framework.router import main_router


def startserver(port: int | str = ServerConf.port, mode: str = "normal"):
    match mode:
        case "normal":
            application = Application(routes=main_router, fronts=applied_middleware, debug_mode=False)
        case "debug":
            application = Application(routes=main_router, fronts=applied_middleware, debug_mode=True)
        case "fake":
            application = FakeApplication(routes=main_router, fronts=applied_middleware)
        case _:
            application = Application(routes=main_router, fronts=applied_middleware, debug_mode=DEBUG_MODE)
    port = int(port) or ServerConf.port

    with make_server("", port, application) as http_server:
        print(f"Serving on port {port}...")
        http_server.serve_forever()
