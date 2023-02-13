from functools import wraps
from inspect import isclass
from time import time
from typing import Callable

from wsgi_framework.router import main_router, prettify_url


def route(url: str | tuple | None):
    """Регистрирует представление в роутере фреймворка.
    Подходит для представлений на базе функций и классов.
    Для обработки ошибки 404 используйте значение параметра url=None.

    Args:
        url (str | tuple | None): строка или кортеж путей, только ASCII, символы "/" в начале и конце добавляются автоматически.
    """

    def decorator(callable: Callable):
        urls = url
        if isinstance(url, list):
            urls = tuple(url)
        urls = urls if isinstance(urls, tuple) else (urls,)
        for curr_url in urls:
            if curr_url and not curr_url.isascii():
                raise ValueError('Путь должен состоять только из латинских букв и символа "/"')
            main_router[prettify_url(curr_url)] = callable() if isclass(callable) else callable

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
