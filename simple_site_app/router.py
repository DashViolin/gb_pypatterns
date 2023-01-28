from .views import About, Categories, CopyCourse, Courses, CreateCategory, CreateCourse, Index, NotFound404, Programs

routes = {
    "/": Index(),
    "/index/": Index(),
    "/about/": About(),
    "/programs/": Programs(),
    "/categories/": Categories(),
    "/categories-create/": CreateCategory(),
    "/courses/": Courses(),
    "/courses-create/": CreateCourse(),
    "/courses-copy/": CopyCourse(),
    None: NotFound404(),
}
