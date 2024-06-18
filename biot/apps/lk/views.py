from django.views import generic


class Home(generic.TemplateView):
    """Домашняя страница."""
    template_name = 'lk/home.html'
