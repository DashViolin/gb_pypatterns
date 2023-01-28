from copy import deepcopy

from wsgi_framework.creational_patterns.category import Category
from wsgi_framework.creational_patterns.constants import interactive_course, record_course


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name: str, category: Category):
        self.name = name
        self.category = category
        self.category.add_course(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {interactive_course: InteractiveCourse, record_course: RecordCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
