from wsgi_framework.architectural_system_patterns.category_mapper import CategoryMapper
from wsgi_framework.architectural_system_patterns.db_exceptions import (
    DbCommitException,
    DbDeleteException,
    DbUpdateException,
    RecordNotFoundException,
)
from wsgi_framework.creational_patterns.courses import Course


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
