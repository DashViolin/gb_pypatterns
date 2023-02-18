from datetime import datetime
from pathlib import Path

from wsgi_framework.creational_patterns.singleton import SingletonByNameMeta


class BaseWriter:
    @staticmethod
    def get_log_entry(message):
        return f"[{datetime.now().replace(microsecond=0)}] --> {message}\n"


class ConsoleWriter(BaseWriter):
    def write(self, message):
        text = self.get_log_entry(message)
        print(text)


class FileWriter(BaseWriter):
    def __init__(self, log_path: str | Path):
        self.log_path = log_path

    def write(self, message):
        text = self.get_log_entry(message)
        with open(self.log_path, "a", encoding="utf8") as f:
            f.write(text)


class Logger(metaclass=SingletonByNameMeta):
    def __init__(self, name: str):
        self.name = name
        self.writers = []

    def add_writer(self, writer):
        self.writers.append(writer)

    def log(self, message: str):
        for writer in self.writers:
            writer.write(message)
