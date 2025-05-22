from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail import hooks

from crm.models import (
    Entity,
    Contact,
    Company,
    Lead,
    Email,
    PhoneNumber,
    Address,
    Website,
    SearchLocation,
    Vertical,
    Outreach,
    OutreachEmail,
    OutreachWebsite,
    CompanyContact,
)


class EntityViewSet(SnippetViewSet):
    model = Entity
    menu_label = "Entities"
    menu_icon = "user"
    list_display = ("name", "is_company")
    filterset_fields = ("is_company",)
    # Panels for editing Entity and related inlines:
    panels = [
        FieldPanel("name"),
        FieldPanel("is_company"),
        FieldPanel("notes"),
        InlinePanel("entityemail_set", label="Emails"),
        InlinePanel("entityphonenumber_set", label="Phone Numbers"),
        InlinePanel("entityaddress_set", label="Addresses"),
        InlinePanel("entitywebsite_set", label="Websites"),
        InlinePanel("entitysearchlocation_set", label="Search Locations"),
        InlinePanel("entityvertical_set", label="Verticals"),
        InlinePanel("entitycontact_set", label="Contacts"),
    ]


class ContactViewSet(SnippetViewSet):
    model = Contact
    menu_label = "Contacts"
    menu_icon = "user"
    list_display = ("first_name", "last_name", "job_title", "linkedin")


class CompanyContactInlinePanel(InlinePanel):
    model = CompanyContact
    extra = 1


class CompanyViewSet(SnippetViewSet):
    model = Company
    menu_label = "Companies"
    menu_icon = "group"
    list_display = ("name", "registration_number")
    panels = [
        FieldPanel("name"),
        FieldPanel("registration_number"),
        FieldPanel("entity"),
        InlinePanel("companycontact_set", label="Contacts"),
    ]


class LeadViewSet(SnippetViewSet):
    model = Lead
    menu_label = "Leads"
    menu_icon = "user"
    list_display = ("first_name", "last_name", "status")


class OutreachEmailInlinePanel(InlinePanel):
    model = OutreachEmail
    extra = 1


class OutreachWebsiteInlinePanel(InlinePanel):
    model = OutreachWebsite
    extra = 1


class OutreachViewSet(SnippetViewSet):
    model = Outreach
    menu_label = "Outreach"
    menu_icon = "mail"
    list_display = ("campaign_search_parameter", "date", "medium")
    panels = [
        FieldPanel("campaign_search_parameter"),
        FieldPanel("date"),
        FieldPanel("medium"),
        OutreachEmailInlinePanel("outreachemail_set", label="Emails"),
        OutreachWebsiteInlinePanel("outreachwebsite_set", label="Websites"),
    ]


class EmailViewSet(SnippetViewSet):
    model = Email
    menu_label = "Emails"
    menu_icon = "mail"
    list_display = ("email",)


class PhoneNumberViewSet(SnippetViewSet):
    model = PhoneNumber
    menu_label = "Phone Numbers"
    menu_icon = "site"
    list_display = ("number",)


class AddressViewSet(SnippetViewSet):
    model = Address
    menu_label = "Addresses"
    menu_icon = "home"
    list_display = ("address_line_1", "city", "postcode")


class WebsiteViewSet(SnippetViewSet):
    model = Website
    menu_label = "Websites"
    menu_icon = "site"
    list_display = ("url",)


class SearchLocationViewSet(SnippetViewSet):
    model = SearchLocation
    menu_label = "Search Locations"
    menu_icon = "location"
    list_display = ("name",)


class VerticalViewSet(SnippetViewSet):
    model = Vertical
    menu_label = "Verticals"
    menu_icon = "list-ul"
    list_display = ("name",)
