from django.urls import path
from apps.lk.views import Home

from .views import UsersListView

app_name = 'lk'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('people', UsersListView.as_view(), name='people'),
    # path('login/', UserLoginView.as_view(), name='login'),

]
