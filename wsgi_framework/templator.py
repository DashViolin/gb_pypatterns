from jinja2 import Environment, FileSystemLoader

from settings import TEMPLATES_DIR


def render(template_name, **kwargs) -> str:
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры контекста для шаблона
    :return: отрендеренный шаблон в виде строки
    """

    templateLoader = FileSystemLoader(searchpath=str(TEMPLATES_DIR))
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template(template_name)
    return template.render(**kwargs)
