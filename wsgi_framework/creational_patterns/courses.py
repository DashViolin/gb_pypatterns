from copy import deepcopy

from wsgi_framework.architectural_system_patterns.unit_or_work import DomainObject
from wsgi_framework.behavioral_patterns.observer import Subject
from wsgi_framework.creational_patterns.constants import interactive_course, record_course
from wsgi_framework.creational_patterns.users import Student


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject, DomainObject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.add_course(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            student.courses.append(self)
        self.notify()

    def __str__(self) -> str:
        return f"Курс: {self.name}"

    def __iter__(self):
        return iter(self.students)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {interactive_course: InteractiveCourse, record_course: RecordCourse}

    @classmethod
    def create(cls, type_, name, category) -> InteractiveCourse | RecordCourse:
        return cls.types[type_](name, category)
