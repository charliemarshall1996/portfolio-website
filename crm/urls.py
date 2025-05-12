from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("api/add-contact/", views.add_contacts, name="add_contact"),
]
