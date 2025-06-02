
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
        InlinePanel("companies"),
        MultiFieldPanel(
            (FieldPanel("linkedin"),),
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
        MultiFieldPanel(
            (FieldPanel("linkedin"),),
            heading="Contact Info"
        )
    ]
    list_display = ["first_name", "last_name", "job_title", "status"]


class EntitySnippet(SnippetViewSet):
    model = Entity
    panels = [
        FieldPanel("campaign_search_parameter", read_only=True),
        FieldPanel("name"),
        FieldPanel("is_company"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        MultiFieldPanel(
            (
                InlinePanel("addresses"),
                InlinePanel("emails"),
                InlinePanel("phone_numbers"),
                InlinePanel("websites")
            ), heading="Contact Info"
        )
    ]


class ContactsAndEntitiesViewsetGroup(SnippetViewSetGroup):
    items = [ContactSnippet, LeadSnippet, EntitySnippet]
    icon = "group"
    menu_icon = "group"
    menu_name = "contacts_and_entities"
    menu_label = "Contacts & Entities"
