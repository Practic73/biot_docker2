from django.urls import path
from apps.eisot import views

app_name = 'eisot'

urlpatterns = [
    path('reestrot/<int:pk>/', views.ReestrOtDetail.as_view(), name='detail'),
    path('reestrots/', views.ReestrOtList.as_view(), name='list'),
]
