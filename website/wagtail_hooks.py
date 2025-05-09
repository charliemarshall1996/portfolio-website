from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from . import models


class WebsiteSnippet(SnippetViewSet):
    model = models.Website
    list_display = ("contact_id", "url")
    panels = [
        FieldPanel("url")
    ]


class AnalysisSnippet(SnippetViewSet):
    model = models.Analysis
    list_display = ("created_at", "website__url",
                    "report_url", "access_token")
    panels = [
        FieldPanel("data")
    ]


class WebsiteSnippetGroup(SnippetViewSetGroup):
    items = (WebsiteSnippet, AnalysisSnippet)
    menu_icon = "globe"
    menu_label = "Website Analysis"
    menu_name = "website-analysis"


register_snippet(WebsiteSnippetGroup)
