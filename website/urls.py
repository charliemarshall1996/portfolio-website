from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("audit/<uuid:token>/", views.audit_view, name="audit_view"),
]
