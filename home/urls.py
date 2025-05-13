from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("services/", views.services_view, name="services"),
    path("get-csrf/", views.get_csrf_token, name="get-csrf")
]
