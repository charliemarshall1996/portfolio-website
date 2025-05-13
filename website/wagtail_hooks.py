from wagtail.admin.panels import FieldPanel, AdminDateTimeInput
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


class EmailSnippet(SnippetViewSet):
    model = models.Email
    list_display = ("email", "last_emailed", "opt_out", "bounced")
    panels = [
        FieldPanel("email"),
        FieldPanel("opt_out"),
        FieldPanel("bounced"),
        AdminDateTimeInput("last_emailed")
    ]


class WebsiteSnippetGroup(SnippetViewSetGroup):
    items = (WebsiteSnippet, AnalysisSnippet, EmailSnippet)
    menu_icon = "globe"
    menu_label = "Website Analysis"
    menu_name = "website-analysis"


register_snippet(WebsiteSnippetGroup)
