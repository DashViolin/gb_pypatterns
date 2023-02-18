from sqlite3 import connect

from wsgi_framework.architectural_system_patterns.category_mapper import CategoryMapper
from wsgi_framework.architectural_system_patterns.course_mapper import CourseMapper
from wsgi_framework.architectural_system_patterns.create_db import create_db
from wsgi_framework.architectural_system_patterns.student_mapper import StudentMapper
from wsgi_framework.config import SQLITE_DB_INIT_SCRIPT_PATH, SQLITE_DB_PATH
from wsgi_framework.creational_patterns.category import Category
from wsgi_framework.creational_patterns.courses import Course
from wsgi_framework.creational_patterns.users import Student

if not SQLITE_DB_PATH.exists():
    create_db(SQLITE_DB_PATH, SQLITE_DB_INIT_SCRIPT_PATH)

data_mapper_connection = connect(SQLITE_DB_PATH)


class MapperRegistry:
    connection = data_mapper_connection
    mappers = {
        "student": StudentMapper,
        "category": CategoryMapper,
        "course": CourseMapper,
    }

    @classmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(MapperRegistry.connection)
        if isinstance(obj, Category):
            return Category(MapperRegistry.connection)
        if isinstance(obj, Course):
            return StudentMapper(MapperRegistry.connection)

    @classmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](MapperRegistry.connection)
