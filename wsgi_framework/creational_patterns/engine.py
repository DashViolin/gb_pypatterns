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

    def create_user(self, type_: str, name: str) -> Student | Teacher:
        user = UserFactory.create(type_, name)
        if isinstance(user, Student):
            self.students.append(user)
        else:
            self.teachers.append(user)

    def create_course(self, type_: str, name: str, category: Category) -> InteractiveCourse | RecordCourse:
        course = CourseFactory.create(type_, name, category)
        self.courses.append(course)
        return course

    def create_category(self, name, category: Category = None) -> Category:
        category = Category(name, category)
        self.categories.append(category)
        return category

    def find_category_by_id(self, id_: int | str | None):
        id_ = int(id_) if isinstance(id_, str) else id_
        for category in self.categories:
            if category.id == id_:
                return category
        return None

    def get_course_by_name(self, name: str) -> InteractiveCourse | RecordCourse:
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
