from django.views.generic import TemplateView


class HomeTestApp(TemplateView):
    template_name="testapp/home.html"