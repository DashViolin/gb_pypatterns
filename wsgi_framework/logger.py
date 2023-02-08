from datetime import datetime

from wsgi_framework.creational_patterns.singleton import SingletonByNameMeta


class Logger(metaclass=SingletonByNameMeta):
    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{datetime.now().replace(microsecond=0)}] LOGGER: '{self.name}' -->", message)
