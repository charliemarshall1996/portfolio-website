from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("companies/", views.CompanyListView.as_view(), name="companies"),
]
