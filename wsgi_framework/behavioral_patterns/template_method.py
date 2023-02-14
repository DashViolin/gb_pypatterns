from wsgi_framework.templator import render


class TemplateView:
    template = ""
    context = {}

    def __init__(self) -> None:
        self.app_name = self.__module__.split(".")[0]

    @staticmethod
    def get_query_data(request):
        return request["query"]

    def process_query(self, query: dict):
        pass

    def get_context_data(self):
        return self.context

    def get_template(self):
        return self.template

    def render_template_with_context(self):
        context = self.get_context_data()
        return "200 OK", render(self.get_template(), self.app_name, **context)

    def __call__(self, request):
        query = self.get_query_data(request)
        self.process_query(query)
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    context_object_name = "objects_list"

    def get_context_data(self):
        self.context[self.context_object_name] = self.queryset
        return super().get_context_data()


class CreateView(ListView):
    @staticmethod
    def get_request_data(request):
        return request["data"]

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request["method"] == "POST":
            query = self.get_query_data(request)
            self.process_query(query)
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)
