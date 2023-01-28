from wsgi_framework.creational_patterns.engine import Engine
from wsgi_framework.creational_patterns.logger import Logger
from wsgi_framework.templator import render

site = Engine()
logger = Logger("main")


class NotFound404:
    def __call__(self, request: dict):
        template = "not_found.html"
        context = {
            "set_active": "index",
        }
        return "404 Not Found", render(template, **context)


class Index:
    def __call__(self, request: dict):
        logger.log("Главная")

        template = "index.html"
        context = {
            "set_active": "index",
            "categories": site.categories,
        }
        return "200 OK", render(template, **context)


class About:
    def __call__(self, request: dict):
        logger.log("Контакты")

        template = "about.html"
        context = {"set_active": "about"}
        return "200 OK", render(template, **context)


class Programs:
    def __call__(self, request: dict):
        logger.log("Программы обучения")

        template = "list_programs.html"
        context = {
            "set_active": "programs",
            "date": request["date"],
        }
        return "200 OK", render(template, **context)


class Categories:
    def __call__(self, request: dict):
        logger.log("Список категорий")

        template = "list_categories.html"
        context = {
            "set_active": "categories",
            "categories": site.categories,
        }
        return "200 OK", render(template, **context)


class CreateCategory:
    def __call__(self, request: dict):
        logger.log("Создание категории")

        if request["method"] == "POST":
            template = "create_category.html"
            name = site.decode_value(request["name"])
            category = site.find_category_by_id(request.get("category_id"))
            site.create_category(name, category)
        else:
            template = "create_category.html"
        context = {
            "set_active": "categories",
            "categories": site.categories,
        }
        return "200 OK", render(template, **context)


class Courses:
    def __call__(self, request: dict):
        logger.log("Список курсов")

        template = "list_courses.html"
        category = site.find_category_by_id(request.get("id"))
        context = {
            "set_active": "courses",
            "category": category,
            "courses": category.courses if category else site.courses,
        }
        return "200 OK", render(template, **context)


class CreateCourse:
    category_id = -1

    def __call__(self, request: dict):
        logger.log("Создание курса")

        if request["method"] == "POST":
            template = "list_courses.html"
            name = site.decode_value(request["name"])
            course_type = request["course_type"]
            category = site.find_category_by_id(self.category_id)
            site.create_course(course_type, name, category)
        else:
            template = "create_course.html"
            self.category_id = request["id"]

        category = site.find_category_by_id(self.category_id)
        context = {
            "set_active": "courses",
            "category": category,
            "courses": category.courses if category else None,
            "courses_types": site.courses_types,
        }
        return "200 OK", render(template, **context)


class CopyCourse:
    def __call__(self, request: dict):
        logger.log("Копирование курса")
        template = "list_courses.html"
        context = {
            "set_active": "courses",
            "courses": site.courses,
        }

        name = request.get("course_name")
        old_course = site.get_course_by_name(name)
        if old_course:
            new_course = old_course.clone()
            new_course.name = f"copy_{name}"
            site.courses.append(new_course)
            context["category"] = new_course.category.name

        return "200 OK", render(template, **context)
