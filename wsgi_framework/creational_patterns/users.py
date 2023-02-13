from abc import ABC

from wsgi_framework.creational_patterns.constants import student_type, teacher_type


class User(ABC):
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {student_type: Student, teacher_type: Teacher}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)
