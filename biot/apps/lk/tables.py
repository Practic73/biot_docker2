from django.contrib.auth import get_user_model

import django_tables2 as tables

User = get_user_model()


class UsersTables(tables.Table):
    class Meta:
        model = User
        template_name = 'django_tables2/bootstrap5.html'
        """ order_by_field = ['snils', 'first_name'] """
        exclude = ('password', )
