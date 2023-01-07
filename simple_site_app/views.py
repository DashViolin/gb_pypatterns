from wsgi_framework.templator import render

sidebar_links = [
    {"name": "Link 1", "href": "#"},
    {"name": "Link 2", "href": "#"},
    {"name": "Link 3", "href": "#"},
]


def index_view(request):
    template = "index.html"
    browsers = [
        "Internet Explorer 8",
        "Internet Explorer 7",
        "FireFox 3.5",
        "Google Chrome 6",
        "Safari 4",
    ]
    context = {
        "set_active": "index",
        "title": "Welcome",
        "browsers": browsers,
        "sidebar_links": sidebar_links,
    }
    return "200 OK", render(template, **context)


def page_view(request):
    template = "page.html"
    text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui."
    context = {
        "set_active": "page",
        "title": "Page",
        "content_title": "Another Page",
        "paragraphs": [text] * 6,
        "sidebar_links": sidebar_links,
    }
    return "200 OK", render(template, **context)


def about_view(request):
    template = "about.html"
    context = {
        "set_active": "about",
        "title": "About",
        "sidebar_links": sidebar_links,
    }
    return "200 OK", render(template, **context)


def not_found_view(request):
    template = "not_found.html"
    context = {
        "title": "Not Found",
        "sidebar_links": sidebar_links,
    }
    return "404 Not Found", render(template, **context)
