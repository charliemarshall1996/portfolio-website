from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("/companies", views.CompanyListView.as_view(), name="companies"),
    path("/company/<int:pk>", views.CompanyDetailView.as_view(), name="company"),
    path("/company/update/<int:pk>",
         views.CompanyUpdateView.as_view(), name="company-update"),
    path("/company/create", views.CompanyCreateView.as_view(), name="company-create"),
    path("/contacts", views.ContactListView.as_view(), name="contacts"),
    path("/contact/<int:pk>", views.ContactDetailView.as_view(), name="contact"),
    path("/contact/update/<int:pk>",
         views.ContactUpdateView.as_view(), name="contact-update"),
    path("/contact/create", views.ContactCreateView.as_view(), name="contact-create"),
]
