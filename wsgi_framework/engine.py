from wsgi_framework.architectural_system_patterns.mapper_registry import MapperRegistry
from wsgi_framework.architectural_system_patterns.models import (
    Category,
    Course,
    CourseFactory,
    InteractiveCourse,
    RecordCourse,
    Student,
    Teacher,
    UserFactory,
)
from wsgi_framework.architectural_system_patterns.unit_or_work import UnitOfWork
from wsgi_framework.creational_patterns.constants import COURSE_TYPES, USER_TYPES

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


class Engine:
    # pattern - identity map
    _students = []
    _categories = []
    _courses = []

    def __init__(self):
        self.courses_types = COURSE_TYPES
        self.users_types = USER_TYPES

    @property
    def teachers(self) -> list:
        return []

    @property
    def students(self) -> list[Student]:
        if self._students:
            mapper = MapperRegistry.get_mapper("student")
            self._students = mapper.all()
        return self._students

    @property
    def categories(self) -> list[Category]:
        if not self._categories:
            mapper = MapperRegistry.get_mapper("category")
            self._categories = mapper.all()
            self.match_courses()
        return self._categories

    @property
    def courses(self) -> list[Course]:
        if not self._courses:
            mapper = MapperRegistry.get_mapper("course")
            self._courses = mapper.all()
            self.match_courses()
        return self._courses

    def match_courses(self):
        for course in self._courses:
            category = self.find_category_by_id(course.category.id)
            category.add_course(course)

    def clean_cache(self):
        self._categories = []
        self._courses = []
        self._students = []

    def create_user(self, type_: str, name: str) -> Student | Teacher:
        user = UserFactory.create(type_, name)
        if isinstance(user, Student):
            user.mark_new()
            UnitOfWork.get_current().commit()
            self._students.append(user)

    def create_course(
        self, type_: str, name: str, category: Category, id: int = None
    ) -> InteractiveCourse | RecordCourse:
        course = CourseFactory.create(type_=type_, name=name, category=category, id=id)
        course.mark_new()
        UnitOfWork.get_current().commit()
        self.clean_cache()
        return course

    def clone_course(self, old_course: Course, new_name: str = None) -> Course:
        new_course = old_course.clone()
        new_course.name = new_name if new_name else f"clone_{new_course.name}"
        new_course.mark_new()
        UnitOfWork.get_current().commit()
        self.clean_cache()
        return new_course

    def create_category(self, name, category: Category = None) -> Category:
        category = Category(name=name, category=category)
        category.mark_new()
        UnitOfWork.get_current().commit()
        self.clean_cache()
        return category

    def add_student_to_course(self, student: Student, course: Course):
        course.add_student(student)

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

    def find_course_by_id(self, id_: int | str | None):
        id_ = int(id_) if isinstance(id_, str) else id_
        for course in self.courses:
            if course.id == id_:
                return course
        return None

    def edit_course(self, edited_course: Course):
        edited_course.mark_dirty()
        UnitOfWork.get_current().commit()
        self.clean_cache()

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
