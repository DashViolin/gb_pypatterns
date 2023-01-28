from abc import ABC

from wsgi_framework.creational_patterns.constants import student_type, teacher_type


class User(ABC):
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {student_type: Student, teacher_type: Teacher}

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()
