from datetime import datetime


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        cls.__instance = {}
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name not in cls.__instance:
            cls.__instance[name] = super().__call__(*args, **kwargs)
        return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{datetime.now().replace(microsecond=0)}] LOGGER: '{self.name}' -->", message)
