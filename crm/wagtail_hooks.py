
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from . import models


class ContactViewSet(SnippetViewSet):
    model = models.Client
    menu_label = "Contacts"
    icon = "user"
    list_display = ("first_name", "last_name", "company", "email", "phone")
    list_filter = ("company",)
    search_fields = ("first_name", "last_name", "email", "company__name")


class CRMViewSetGroup(SnippetViewSetGroup):
    menu_label = "CRM"
    menu_icon = "folder"
    menu_order = 200
    items = (ContactViewSet,)


class WebsiteSnippet(SnippetViewSet):
    model = models.Website
    list_display = ("contact_id", "url")
    panels = [FieldPanel("url")]


class AnalysisSnippet(SnippetViewSet):
    model = models.Analysis
    list_display = ("created_at", "website__url", "report_url", "access_token")
    panels = [FieldPanel("data")]


class WebsiteSnippetGroup(SnippetViewSetGroup):
    items = (WebsiteSnippet, AnalysisSnippet)
    menu_icon = "globe"
    menu_label = "Website Analysis"
    menu_name = "website-analysis"


register_snippet(WebsiteSnippetGroup)
register_snippet(CRMViewSetGroup)
