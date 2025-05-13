from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("services/", views.services_view, name="services"),
    path("api/auth/", views.api_auth_view, name="api-auth")
]
