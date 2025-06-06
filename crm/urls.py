from django.urls import path

from . import api

app_name = "crm"

urlpatterns = [
    path("api/auth/", api.api_auth_view, name="authentication"),
    path("api/params/", api.search_parameter_view, name="search_parameters"),
    path("api/lead/", api.add_lead_view, name="add_lead"),
    path("api/email/", api.brevo_webhook_view, name="email"),
]
