from sqlite3 import connect

from wsgi_framework.architectural_system_patterns.create_db import create_db
from wsgi_framework.architectural_system_patterns.data_mapper import CategoryMapper, CourseMapper, StudentMapper
from wsgi_framework.config import SQLITE_DB_INIT_SCRIPT_PATH, SQLITE_DB_PATH

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
    def get_mapper(name):
        return MapperRegistry.mappers[name](MapperRegistry.connection)
