from .views import CopyCourse, CreateCategory, CreateCourse

"""
Адреса, задаваемые в данном файле, имеют высший приоритет по отношению к адресам, 
регистрируемым с использованием декоратора route
"""

routes = {
    "/categories-create/": CreateCategory,
    "/courses-create/": CreateCourse,
    "/courses-copy/": CopyCourse,
}
