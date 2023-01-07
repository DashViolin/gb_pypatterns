def test():
    import importlib

    i = importlib.import_module("simple_site.router")
    print(i.routes)
