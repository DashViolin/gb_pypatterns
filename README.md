# gb_pypatterns

GeekBrains patterns course (simple WSGI framework)

## Запуск сервера

1. Установить зависимости из **pyproject.toml** (poetry, pipenv) или **requirements.txt** (virtualenv + pip).
2. Активировать виртуальное окружение.
3. Перейти в корень проекта.
4. Запустить команду ``python manage.py startserver [номер_порта]``, по умолчанию сервер запускается на ``8000``. Можно также запустить ``python run.py``, меньше писать, внутри он все-равно вызывает в отдельном процессе ``python manage.py startserver``.
5. Перейти в браузере по адресу ``127.0.0.1:номер_порта``.
