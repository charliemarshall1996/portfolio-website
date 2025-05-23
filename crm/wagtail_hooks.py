from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail import hooks

from . import models


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


class CompanyContactInlinePanel(InlinePanel):
    model = models.CompanyContact
    extra = 1


class CompanyViewSet(SnippetViewSet):
    model = models.Company
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
    model = models.Lead
    menu_label = "Leads"
    menu_icon = "user"
    list_display = ("first_name", "last_name", "status")


class OutreachEmailInlinePanel(InlinePanel):
    model = models.OutreachEmail
    extra = 1


class OutreachWebsiteInlinePanel(InlinePanel):
    model = models.OutreachWebsite
    extra = 1


class OutreachViewSet(SnippetViewSet):
    model = models.Outreach
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


class CampaignViewSet(SnippetViewSet):
    model = models.Campaign
    panels = [
        FieldPanel("type"),
        FieldPanel("medium"),
        FieldPanel("description"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("is_active"),
        MultiFieldPanel(
            (
                FieldPanel("vertical"),
                InlinePanel("search_locations", label="locations"),
            ),
            heading="Search Parameters",
        ),
        MultiFieldPanel(
            (
                InlinePanel(
                    "email_content", label="Email Content", max_num=5, min_num=5
                ),
            ),
            heading="Conent",
        ),
    ]
    list_display = ["start_date", "end_date", "type", "medium", "is_active"]


class CampaignViewSetGroup(SnippetViewSetGroup):
    items = [
        CampaignViewSet,
    ]
    menu_icon = "calendar-alt"
    menu_name = "campaign"
    menu_label = "Campaign"
