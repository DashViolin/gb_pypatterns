from functools import wraps
from inspect import isclass
from time import time
from typing import Callable

from wsgi_framework.router import main_router, prettiry_url


def route(url: str | None):
    """Регистрирует представление в роутере фреймворка.
    Подходит для представлений на базе функций и классов.
    Для обработки ошибки 404 используйте значение параметра url=None.

    Args:
        url (str | None): строка пути, только ASCII, символы "/" в начале и конце добавляются автоматически.
    """

    def decorator(callable: Callable):
        if url and not url.isascii():
            raise ValueError('Путь должен состоять только из латинских букв и символа "/"')

        main_router[prettiry_url(url)] = callable() if isclass(callable) else callable

        @wraps(callable)
        def wrapper(*args, **kwargs):
            return callable(*args, **kwargs)

        return wrapper

    return decorator


def debug(callable: Callable):
    """
    Выводит в консоль название представления и время его выполнения.
    Подходит для функций и методов классов.
    """

    @wraps(callable)
    def wrapper(*args, **kwargs):
        ts = time()
        result = callable(*args, **kwargs)
        te = time()
        print(f"[DEBUG] --> View: {callable.__qualname__.split('.')[0]} -- time: {(te - ts):2.3f} ms.")
        return result

    return wrapper
