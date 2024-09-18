from django.views import generic
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_tables2 import SingleTableView

from .tables import UsersTables

User = get_user_model()


class Home(generic.TemplateView):
    """Домашняя страница."""
    template_name = 'lk/home.html'


class UsersListView(SingleTableView):
    model = User
    table_class = UsersTables
    template_name = 'lk/users.html'
