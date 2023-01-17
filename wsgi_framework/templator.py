import inspect

from jinja2 import Environment, FileSystemLoader

from wsgi_framework.config import APP_TEMPLATES_DIR_NAME, BASE_DIR, BASE_STATIC_PATH, BASE_TEMPLATES_PATH


def render(template_name, **kwargs) -> str:
    """
    Функция рендеринга HTML на базе шаблона
    :param template_name: имя шаблона
    :param kwargs: параметры контекста для шаблона
    :return: отрендеренный шаблон в виде строки
    """
    caller_function = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_function[0])
    app_name = caller_module.__name__.split(".")[0]
    app_templates_folder = str(BASE_DIR / app_name / APP_TEMPLATES_DIR_NAME)

    base_templates_folder = str(BASE_TEMPLATES_PATH)
    base_static_folder = str(BASE_STATIC_PATH)

    templateLoader = FileSystemLoader([base_templates_folder, base_static_folder, app_templates_folder])
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(template_name)
    return template.render(**kwargs)
