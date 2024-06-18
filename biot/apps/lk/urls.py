from django.urls import path
from apps.lk.views import Home

app_name = 'lk'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # path('login/', UserLoginView.as_view(), name='login'),
]
