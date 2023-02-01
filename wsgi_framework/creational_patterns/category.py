class Category:
    auto_id = 0

    def __init__(self, name, category=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def add_course(self, course):
        self.courses.append(course)
