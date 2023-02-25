from sqlite3 import connect

from wsgi_framework.architectural_system_patterns.create_db import create_db
from wsgi_framework.architectural_system_patterns.data_mappers import CategoryMapper, CourseMapper, StudentMapper
from wsgi_framework.architectural_system_patterns.models import Category, Course, Student
from wsgi_framework.config import SQLITE_DB_INIT_SCRIPT_PATH, SQLITE_DB_PATH

if not SQLITE_DB_PATH.exists():
    create_db(SQLITE_DB_PATH, SQLITE_DB_INIT_SCRIPT_PATH)


class MapperRegistry:
    connection = connect(SQLITE_DB_PATH)
    mappers = {
        "student": StudentMapper,
        "category": CategoryMapper,
        "course": CourseMapper,
    }

    @classmethod
    def get_mapper(cls, mapper):
        if isinstance(mapper, str):
            return cls.mappers[mapper](MapperRegistry.connection)
        if isinstance(mapper, Student):
            return StudentMapper(MapperRegistry.connection)
        if isinstance(mapper, Category):
            return CategoryMapper(MapperRegistry.connection)
        if isinstance(mapper, Course):
            return CourseMapper(MapperRegistry.connection)
