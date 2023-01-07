from .views import about_view, index_view, not_found_view, page_view

routes = {
    "/": index_view,
    "/index/": index_view,
    "/page/": page_view,
    "/about/": about_view,
    None: not_found_view,
}
