from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('<str:date>/', views.BookingAPI.as_view(), name='api')
]
