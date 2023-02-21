from wsgi_framework.architectural_system_patterns.unit_or_work import MapperRegistry, UnitOfWork
from wsgi_framework.creational_patterns.category import Category
from wsgi_framework.creational_patterns.constants import COURSE_TYPES, USER_TYPES
from wsgi_framework.creational_patterns.courses import Course, CourseFactory, InteractiveCourse, RecordCourse
from wsgi_framework.creational_patterns.users import Student, Teacher, UserFactory

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


class Engine:
    def __init__(self):
        self.courses_types = COURSE_TYPES
        self.users_types = USER_TYPES

    @property
    def students(self) -> list[Student]:
        mapper = MapperRegistry.get_mapper("student")
        return mapper.all()

    @property
    def teachers(self) -> list:
        return []

    @property
    def categories(self) -> list[Category]:
        mapper = MapperRegistry.get_mapper("category")
        return mapper.all()

    @property
    def courses(self) -> list[Course]:
        mapper = MapperRegistry.get_mapper("course")
        return mapper.all()

    def create_user(self, type_: str, name: str) -> Student | Teacher:
        user = UserFactory.create(type_, name)
        if isinstance(user, Student):
            user.mark_new()
            UnitOfWork.get_current().commit()
        else:
            pass

    def create_course(self, type_: str, name: str, category: Category) -> InteractiveCourse | RecordCourse:
        course = CourseFactory.create(type_, name, category)
        course.mark_new()
        UnitOfWork.get_current().commit()
        return course

    def create_category(self, name, category: Category = None) -> Category:
        category = Category(name, category)
        category.mark_new()
        UnitOfWork.get_current().commit()
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

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
