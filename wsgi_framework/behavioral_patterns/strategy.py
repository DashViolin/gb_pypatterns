from abc import ABC, abstractmethod


class BaseWriter(ABC):
    @abstractmethod
    def write(self, text):
        raise NotImplementedError()


class ConsoleWriter(BaseWriter):
    def write(self, text):
        print(text)


class FileWriter(BaseWriter):
    def __init__(self):
        self.file_name = "log"

    def write(self, text):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
