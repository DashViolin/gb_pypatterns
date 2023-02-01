from quopri import decodestring

from wsgi_framework.creational_patterns.category import Category
from wsgi_framework.creational_patterns.constants import COURSE_TYPES, USER_TYPES
from wsgi_framework.creational_patterns.courses import CourseFactory, InteractiveCourse, RecordCourse
from wsgi_framework.creational_patterns.users import Student, Teacher, UserFactory


class Engine:
    def __init__(self):
        self.courses_types = COURSE_TYPES
        self.users_types = USER_TYPES
        self.teachers: list[Teacher] = []
        self.students: list[Student] = []
        self.categories: list[Category] = []
        self.courses: list[InteractiveCourse | RecordCourse] = []

    @staticmethod
    def decode_value(value: str, encoding: str = "UTF-8") -> str:
        decoded_bytes = decodestring(bytes(value.replace("%", "=").replace("+", " "), encoding))
        return decoded_bytes.decode(encoding)

    def create_user(self, type_: str) -> Student | Teacher:
        user = UserFactory.create(type_)
        if isinstance(user, Student):
            self.students.append(user)
        else:
            self.teachers.append(user)
        return user

    def create_course(self, type_: str, name: str, category: Category) -> InteractiveCourse | RecordCourse:
        course = CourseFactory.create(type_, name, category)
        self.courses.append(course)
        return course

    def create_category(self, name, category: Category = None) -> Category:
        category = Category(name, category)
        self.categories.append(category)
        return category

    def find_category_by_id(self, id_: int | str | None):
        if id_:
            id_ = id_ if isinstance(id_, int) else int(id_)
            for category in self.categories:
                if category.id == id_:
                    return category
        return None

    def get_course_by_name(self, name: str) -> InteractiveCourse | RecordCourse:
        for course in self.courses:
            if course.name == name:
                return course
        return None
