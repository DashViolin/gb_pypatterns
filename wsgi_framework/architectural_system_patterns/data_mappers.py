from wsgi_framework.architectural_system_patterns.db_exceptions import (
    DbCommitException,
    DbDeleteException,
    DbUpdateException,
    RecordNotFoundException,
)
from wsgi_framework.architectural_system_patterns.models import Category, Course, Student


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = "category"

    def all(self) -> list[Category]:
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, parent_id = item
            if parent_id:
                for parent_category in result:
                    if parent_category.id == parent_id:
                        category = Category(name=name, id=id, category=parent_category)
            else:
                category = Category(name=name, id=id)
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
            statement = f"INSERT INTO {self.tablename} (name, parent_id) VALUES (?, ?)"
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

    def all(self) -> list[Course]:
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for course_id, name, category_id in self.cursor.fetchall():
            for category in self.categories_mapper.all():
                if category_id == category.id:
                    course = Course(id=course_id, name=name, category=category)
                    result.append(course)
        return result

    def find_by_id(self, id):
        courses = self.all()
        for course in courses:
            if course.id == id:
                return course
        raise RecordNotFoundException(id)

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category_id) VALUES (?, ?)"
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

    def all(self) -> list[Student]:
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name, id)
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
