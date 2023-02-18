from wsgi_framework.architectural_system_patterns.db_exceptions import (
    DbCommitException,
    DbDeleteException,
    DbUpdateException,
    RecordNotFoundException,
)
from wsgi_framework.creational_patterns.category import Category


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
