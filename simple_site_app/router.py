from .views import CopyCourse, CreateCategory, CreateCourse, Index

"""
Адреса, задаваемые в данном файле, имеют высший приоритет по отношению к адресам, 
регистрируемым с использованием декоратора route
"""

routes = {
    "/": Index(),
    "/categories-create/": CreateCategory(),
    "/courses-create/": CreateCourse(),
    "/courses-copy/": CopyCourse(),
}
