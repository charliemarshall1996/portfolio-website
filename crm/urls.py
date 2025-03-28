from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.home_view, name="home"),

    path("/companies", views.CompanyListView.as_view(), name="company-list"),
    path("/company/<int:pk>", views.CompanyDetailView.as_view(),
         name="company-detail"),
    path("/company/update/<int:pk>",
         views.CompanyUpdateView.as_view(), name="company-update"),
    path("/company/create", views.CompanyCreateView.as_view(), name="company-create"),

    path("/contacts", views.ContactListView.as_view(), name="contact-list"),
    path("/contact/<int:pk>", views.ContactDetailView.as_view(),
         name="contact-detail"),
    path("/contact/update/<int:pk>",
         views.ContactUpdateView.as_view(), name="contact-update"),
    path("/contact/create", views.ContactCreateView.as_view(), name="contact-create"),

    path("/interactions", views.InteractionListView.as_view(),
         name="interaction-list"),
    path("/interaction/<int:pk>",
         views.InteractionDetailView.as_view(), name="interaction-detail"),
    path("/interaction/update/<int:pk>",
         views.InteractionUpdateView.as_view(), name="interaction-update"),
    path("/interaction/create", views.InteractionCreateView.as_view(),
         name="interaction-create"),
]
