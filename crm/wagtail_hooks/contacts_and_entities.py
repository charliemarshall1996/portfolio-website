
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import Contact, Lead, Entity


class ContactSnippet(SnippetViewSet):
    model = Contact
    panels = [
        FieldPanel("salutation"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("job_title"),
        FieldPanel("notes"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        InlinePanel("contact_entities"),
        MultiFieldPanel(
            (FieldPanel("linkedin"),
             InlinePanel("contact_emails"),
             InlinePanel("contact_phone_numbers")),
            heading="Contact Info"
        )
    ]
    list_display = ["first_name", "last_name", "job_title"]


class LeadSnippet(SnippetViewSet):
    model = Lead
    panels = [
        FieldPanel("salutation"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("job_title"),
        FieldPanel("status"),
        FieldPanel("notes"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        InlinePanel("lead_entities"),
        MultiFieldPanel(
            (FieldPanel("linkedin"),
             InlinePanel("lead_emails"),
             InlinePanel("lead_phone_numbers")),
            heading="Contact Info"
        )
    ]
    list_display = ["first_name", "last_name", "job_title", "status"]


class EntitySnippet(SnippetViewSet):
    model = Entity
    panels = [
        FieldPanel("vertical"),
        FieldPanel("campaign_search_parameter", read_only=True),
        FieldPanel("name"),
        FieldPanel("is_company"),
        FieldPanel("description"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        MultiFieldPanel(
            (
                InlinePanel("entity_contacts", label="Contacts"),
                InlinePanel("entity_leads", label="Leads")
            ), heading="People"
        ),
        MultiFieldPanel(
            (
                InlinePanel("entity_addresses"),
                InlinePanel("entity_emails"),
                InlinePanel("entity_phone_numbers"),
                InlinePanel("entity_websites")
            ), heading="Contact Info"
        )
    ]


class ContactsAndEntitiesViewsetGroup(SnippetViewSetGroup):
    items = [ContactSnippet, LeadSnippet, EntitySnippet]
    icon = "group"
    menu_icon = "group"
    menu_name = "contacts_and_entities"
    menu_label = "Contacts & Entities"
