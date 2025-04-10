

from django import urls

from . import views

app_name = "crm"

urlpatterns = [
    urls.path("", views.CRMLoginView.as_view(), name="login"),
    urls.path("dashboard/", views.dashboard_view, name="dashboard"),
    urls.path("companies", views.CompanyListView.as_view(),
              name="company-list"),
    urls.path("company/<int:pk>", views.CompanyDetailView.as_view(),
              name="company-detail"),
    urls.path(
        "company/update/<int:pk>",
        views.CompanyUpdateView.as_view(),
        name="company-update",
    ),
    urls.path("company/create", views.CompanyCreateView.as_view(),
              name="company-create"),
    urls.path("contacts", views.ContactListView.as_view(),
              name="contact-list"),
    urls.path("contact/<int:pk>", views.ContactDetailView.as_view(),
              name="contact-detail"),
    urls.path(
        "contact/update/<int:pk>",
        views.ContactUpdateView.as_view(),
        name="contact-update",
    ),
    urls.path("contact/create", views.ContactCreateView.as_view(),
              name="contact-create"),
    urls.path("interactions", views.InteractionListView.as_view(),
              name="interaction-list"),
    urls.path(
        "interaction/<int:pk>",
        views.InteractionDetailView.as_view(),
        name="interaction-detail",
    ),
    urls.path(
        "interaction/update/<int:pk>",
        views.InteractionUpdateView.as_view(),
        name="interaction-update",
    ),
    urls.path(
        "interaction/create",
        views.InteractionCreateView.as_view(),
        name="interaction-create",
    ),
]
