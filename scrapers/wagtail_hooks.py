from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from . import models


class SearchTermSnippet(SnippetViewSet):
    model = models.SearchTerm
    list_display = ("term",)
    panels = [
        FieldPanel("term")
    ]


class LocationSnippet(SnippetViewSet):
    model = models.Location
    list_display = ("name", "type")
    panels = [
        FieldPanel("name"),
        FieldPanel("type")
    ]


class SearchParameters(SnippetViewSet):
    model = models.SearchParameter
    list_display = ("term__term", "location__name", "last_run_freeindex")
    panels = [
        FieldPanel("live")
    ]


class ScraperSnippetGroup(SnippetViewSetGroup):
    items = (SearchTermSnippet, LocationSnippet, SearchParameters)
    menu_icon = "cog"
    menu_label = "Scraper Settings"
    menu_name = "scraper-settings"


register_snippet(ScraperSnippetGroup)
