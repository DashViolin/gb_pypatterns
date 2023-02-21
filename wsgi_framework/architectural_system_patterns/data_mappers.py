from sqlite3 import connect

from wsgi_framework.architectural_system_patterns.create_db import create_db
from wsgi_framework.architectural_system_patterns.db_exceptions import (
    DbCommitException,
    DbDeleteException,
    DbUpdateException,
    RecordNotFoundException,
)
from wsgi_framework.architectural_system_patterns.models import Category, Course, Student
from wsgi_framework.config import SQLITE_DB_INIT_SCRIPT_PATH, SQLITE_DB_PATH

if not SQLITE_DB_PATH.exists():
    create_db(SQLITE_DB_PATH, SQLITE_DB_INIT_SCRIPT_PATH)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "category"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, parent_id = item
            if parent_id:
                for parent_category in result:
                    if parent_category.id == parent_id:
                        category = Category(name, category=parent_category)
            else:
                category = Category(name)
            result.append(category)
        return result

    def find_by_id(self, id):
        categories = self.all()
        for category in categories:
            if category.id == id:
                return category
        raise RecordNotFoundException(id)

    def insert(self, obj):
        if obj.category:
            statement = f"INSERT INTO {self.tablename} (name, parent_id) VALUES (?)"
            values = (obj.name, obj.category.id)
        else:
            statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
            values = (obj.name,)
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        if obj.category:
            statement = f"UPDATE {self.tablename} SET name=?, parent_id=? WHERE id=?"
            values = (obj.name, obj.category.id, obj.id)
        else:
            statement = f"UPDATE {self.tablename} SET name=?, WHERE id=?"
            values = (obj.name, obj.id)
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper:
    def __init__(self, connection):
        self.categories_mapper = CategoryMapper(connection)
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "course"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            for category in self.categories_mapper.all():
                if category.id == item.category_id:
                    course = Course(item.id, category)
                    result.append(course)
        return result

    def find_by_id(self, id):
        courses = self.all()
        for course in courses:
            if course.id == id:
                return course
        raise RecordNotFoundException(id)

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category_id) VALUES (?)"
        values = (obj.name, obj.category.id)
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, category_id=? WHERE id=?"
        values = (obj.name, obj.category.id, obj.id)
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "student"

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f"record with id={id} not found")

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    connection = connect(SQLITE_DB_PATH)
    mappers = {
        "student": StudentMapper,
        "category": CategoryMapper,
        "course": CourseMapper,
    }

    @staticmethod
    def get_mapper(mapper):
        if isinstance(mapper, str):
            return MapperRegistry.mappers[mapper](MapperRegistry.connection)
        if isinstance(mapper, Student):
            return StudentMapper(MapperRegistry.connection)
        if isinstance(mapper, Category):
            return CategoryMapper(MapperRegistry.connection)
        if isinstance(mapper, Course):
            return CourseMapper(MapperRegistry.connection)
