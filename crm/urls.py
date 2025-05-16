from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("api/add-contact/", views.add_contact, name="add_contact"),
    path("audit/<uuid:token>/", views.audit_view, name="audit_view"),
]
