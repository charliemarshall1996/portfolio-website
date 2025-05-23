from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel, InlinePanel

from crm import models


class EntityViewSet(SnippetViewSet):
    model = models.Entity
    menu_label = "Entities"
    menu_icon = "user"
    list_display = ("name", "is_company")
    filterset_fields = ("is_company",)
    # Panels for editing Entity and related inlines:
    panels = [
        FieldPanel("name"),
        FieldPanel("is_company"),
        FieldPanel("notes"),
        InlinePanel("emails", label="Emails"),
        InlinePanel("phone_numbers", label="Phone Numbers"),
        InlinePanel("addresses", label="Addresses"),
        InlinePanel("websites", label="Websites"),
        InlinePanel("locations", label="Search Locations"),
        InlinePanel("verticals", label="Verticals"),
    ]


class ContactViewSet(SnippetViewSet):
    model = models.Contact
    menu_label = "Contacts"
    menu_icon = "user"
    list_display = ("first_name", "last_name", "job_title", "linkedin")
    panels = [
        FieldPanel("salutation"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("job_title"),
        FieldPanel("linkedin"),
        FieldPanel("notes"),
    ]


class CompanyContactInlinePanel(InlinePanel):
    model = models.CompanyContact
    extra = 1


class CompanyViewSet(SnippetViewSet):
    model = models.Company
    menu_label = "Companies"
    menu_icon = "building"
    list_display = ("name", "registration_number")
    panels = [
        FieldPanel("name"),
        FieldPanel("registration_number"),
        FieldPanel("entity", read_only=True),
        InlinePanel("contacts", label="Contacts"),
    ]


class LeadViewSet(SnippetViewSet):
    model = models.Lead
    menu_label = "Leads"
    menu_icon = "user"
    list_display = ("first_name", "last_name",
                    "job_title", "status", "linkedin")
    panels = [
        FieldPanel("salutation"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("job_title"),
        FieldPanel("linkedin"),
        FieldPanel("status"),
        FieldPanel("campaign"),
        FieldPanel("notes"),
    ]


class EntityViewSetGroup(SnippetViewSetGroup):
    items = [EntityViewSet, ContactViewSet, CompanyViewSet, LeadViewSet]
    menu_icon = "group"
    menu_name = "entities"
    menu_label = "Entities"
