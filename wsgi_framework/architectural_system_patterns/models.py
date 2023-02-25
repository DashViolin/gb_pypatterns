from abc import ABC
from copy import deepcopy

from wsgi_framework.architectural_system_patterns.domain_object import DomainObject
from wsgi_framework.behavioral_patterns.observer import Subject
from wsgi_framework.creational_patterns.constants import interactive_course, record_course, student_type, teacher_type


class User(ABC):
    user_id = 1

    def __init__(self, name: str, id: int = None):
        self.id = id or User.user_id
        User.user_id = self.id + 1
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


class Category(DomainObject):
    auto_id = 1

    def __init__(self, name, category: "Category" = None, id: int = None):
        self.id = id or Category.auto_id
        Category.auto_id = self.id + 1
        self.name = name
        self.category: "Category" = category
        self.courses = []

    @property
    def full_name(self):
        name = self.name
        if self.category:
            name = f"{self.category.full_name} / {name}"
        return name

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def add_course(self, course):
        self.courses.append(course)

    def __str__(self) -> str:
        return f"Категория: {self.name}"

    def __iter__(self):
        return iter(self.courses)


class Course(Subject, DomainObject):
    auto_id = 1

    def __init__(self, name, category: Category, id=None):
        self.id = id or Course.auto_id
        Course.auto_id = self.id + 1
        self.name = name
        self.category = category
        self.category.add_course(self)
        self.students = []
        super().__init__()

    def clone(self):
        new_course = deepcopy(self)
        new_course.id = Course.auto_id
        Course.auto_id += 1
        return new_course

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
    def create(cls, type_, name, category, id=None) -> InteractiveCourse | RecordCourse:
        return cls.types[type_](name=name, category=category, id=id)
