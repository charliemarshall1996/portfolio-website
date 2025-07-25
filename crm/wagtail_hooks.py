from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet
from . import models
# Create your views here.


class VerticalViewSet(SnippetViewSet):
    model = models.Vertical
    form_fields = ["name", "description"]
    menu_label = "Verticals"
    list_display = ["name"]


class ContactViewSet(SnippetViewSet):
    model = models.Contact
    form_fields = ["first_name", "last_name", "company", "email", "email_opt_out",
                   "phone", "website", "vertical", "status", "created_at", "updated_at"]
    list_display = ["first_name", "last_name", "company", "email", "website",
                    "vertical", "status", "created_at", "updated_at"]
    menu_label = "Contacts"


class CommunicationViewSet(SnippetViewSet):
    model = models.Communication
    form_fields = ["contact", "medium", "direction", "communication_type", "subject",
                   "body", "made_on", "notes"]
    list_display = ["contact", "medium", "made_on",
                    "direction", "communication_type"]
    menu_label = "Communications"


class CRMViewsetGroup(SnippetViewSetGroup):
    items = [VerticalViewSet, ContactViewSet, CommunicationViewSet]
    menu_name = "crm"
    menu_label = "CRM"
    menu_icon = "mail"


register_snippet(CRMViewsetGroup)
