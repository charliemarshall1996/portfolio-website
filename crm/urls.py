from django.urls import path

from . import views, api

app_name = "crm"

urlpatterns = [
    path("api/auth/", api.api_auth_view, name="authentication"),
    path("api/params/", api.search_parameter_view, name="search_parameters"),
    path("api/lead/", api.add_lead_view, name="add_lead")
]
