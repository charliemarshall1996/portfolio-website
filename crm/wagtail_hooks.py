from django import urls
from wagtail import hooks
from wagtail.admin import menu
from . import views


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
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


@hooks.register('register_admin_menu_item')
def register_company_menu_item():
    return menu.MenuItem('Companies', urls.reverse('company-list'), icon_name='globe')


@hooks.register('register_admin_menu_item')
def register_contact_menu_item():
    return menu.MenuItem('Contacts', urls.reverse('contact-list'), icon_name='group')


@hooks.register('register_admin_menu_item')
def register_interaction_menu_item():
    return menu.MenuItem('Interactions', urls.reverse('interaction-list'),
                         icon_name='mail')
