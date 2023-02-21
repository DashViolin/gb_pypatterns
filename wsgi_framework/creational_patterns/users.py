from abc import ABC

from wsgi_framework.architectural_system_patterns.domain_object import DomainObject
from wsgi_framework.creational_patterns.constants import student_type, teacher_type


class User(ABC):
    user_id = 1

    def __init__(self, name: str, id: int = None):
        self.id = id or self.user_id
        self.user_id += 1
        self.name = name

    def __str__(self) -> str:
        return self.name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name, id: int = None):
        self.courses = []
        super().__init__(name, id)


class UserFactory:
    types = {student_type: Student, teacher_type: Teacher}

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)
