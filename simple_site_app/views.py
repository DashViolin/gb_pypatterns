from wsgi_framework.behavioral_patterns.observer import EmailNotifier, SmsNotifier
from wsgi_framework.behavioral_patterns.serializer import BaseSerializer
from wsgi_framework.behavioral_patterns.template_method import CreateView, ListView
from wsgi_framework.creational_patterns.engine import Engine
from wsgi_framework.logger import ConsoleWriter, FileWriter, Logger
from wsgi_framework.structural_patterns.decorators import route
from wsgi_framework.templator import render

site = Engine()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

console_writer = ConsoleWriter()
file_writer = FileWriter("main.log")
logger = Logger("main")
logger.add_writer(console_writer)
logger.add_writer(file_writer)


@route(url=None)
class NotFound404(ListView):
    template = "not_found.html"
    context = {"set_active": "index"}


@route(url=("/index/", "/"))
class Index(ListView):
    template = "index.html"
    context = {
        "set_active": "index",
        "categories": site.categories,
    }


@route(url="/about")
class About(ListView):
    template = "about.html"
    context = {"set_active": "about"}


@route(url="programs")
class Programs(ListView):
    template = "list_programs.html"
    context = {"set_active": "programs"}


@route(url="categories")
class Categories(ListView):
    template = "list_categories.html"
    queryset = site.categories
    context = {"set_active": "categories"}


class CreateCategory(CreateView):
    template = "create_category.html"
    queryset = site.categories
    context = {"set_active": "categories"}

    def process_query(self, query: dict):
        self.category_id = query.get("category_id")

    def create_obj(self, data):
        name = data["name"]
        category = site.find_category_by_id(self.category_id)
        site.create_category(name, category)


@route(url="/courses")
class Courses(ListView):
    template = "list_courses.html"
    context = {"set_active": "courses"}

    def process_query(self, query: dict):
        category = site.find_category_by_id(query.get("category_id"))
        self.queryset = category.courses if category else site.courses
        self.context["category"] = category


@route(url="/course-edit")
class EditCourse(CreateView):
    template = "edit_course.html"
    context = {"set_active": "courses"}
    course = None

    def process_query(self, query: dict):
        course = site.get_course_by_name(query["course-name"])
        if course:
            self.course = course
            self.queryset = site.categories
            self.context["course"] = self.course

    def create_obj(self, data):
        new_name = data["name"]
        new_category = site.find_category_by_id(data["category_id"])
        logger.log(f"new_name={new_name}, {self.course}, {new_category}")
        self.course.name = new_name
        self.course.category = new_category


class CreateCourse(CreateView):
    category_id = -1

    def __call__(self, request: dict):
        logger.log("Создание курса")

        if request["method"] == "POST":
            template = "list_courses.html"
            name = request["data"]["name"]
            course_type = request["data"]["course_type"]
            category = site.find_category_by_id(self.category_id)
            course = site.create_course(course_type, name, category)
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
        elif request["method"] == "GET":
            category_id = request["query"].get("category_id")
            if category_id:
                template = "create_course.html"
                self.category_id = category_id
            else:
                template = "list_courses.html"

        category = site.find_category_by_id(self.category_id)
        context = {
            "set_active": "courses",
            "category": category,
            "objects_list": category.courses if category else None,
            "courses_types": site.courses_types,
        }
        return "200 OK", render(template, self.app_name, **context)


class CopyCourse(CreateView):
    template = "list_courses.html"
    context = {
        "set_active": "courses",
        "objects_list": site.courses,
    }

    def create_obj(self, data: dict):
        name = data.get("course_name")
        old_course = site.get_course_by_name(name)
        if old_course:
            new_course = old_course.clone()
            new_course.name = f"copy_{name}"
            old_course.category.add_course(new_course)
            site.create_course(new_course)
            self.context["category"] = new_course.category.name


@route(url="/students/")
class StudentListView(ListView):
    queryset = site.students
    template = "list_students.html"
    context = {"set_active": "students"}


@route(url="/create-student/")
class StudentCreateView(CreateView):
    template = "create_student.html"
    context = {"set_active": "students"}

    def create_obj(self, data: dict):
        name = data["student_name"]
        site.create_user("student", name)


@route(url="/add-student/")
class AddStudentToCourseView(CreateView):
    template = "add_student_to_course.html"
    context = {
        "courses": site.courses,
        "students": site.students,
    }

    def create_obj(self, data: dict):
        student = site.get_student(data["student_name"])
        course = site.get_course_by_name(data["course_name"])
        site.add_student_to_course(student, course)


@route(url="/api/")
class CourseApi:
    def __call__(self, request):
        return "200 OK", BaseSerializer(site.courses).save()
