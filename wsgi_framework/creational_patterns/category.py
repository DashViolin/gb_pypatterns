from wsgi_framework.architectural_system_patterns.unit_or_work import DomainObject


class Category(DomainObject):
    auto_id = 1

    def __init__(self, name, category=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category: "Category" = category
        self.courses = []

    @property
    def full_name(self):
        name = self.name
        # if self.category:
        #     name = f'{self.category.full_name} / {name}'
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
