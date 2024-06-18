from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser


class LoginForm(AuthenticationForm):
    # is_soglasie = forms.BooleanField(label='Согласие')

    class Meta:
        model = CustomUser
        fields = ['username', 'password',]
