from wagtail.admin.panels import FieldPanel, InlinePanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import SearchLocation, Vertical, Email


class EmailViewSet(SnippetViewSet):
    model = Email
    panels = [
        FieldPanel("email"),
        FieldPanel("opted_out"),
        FieldPanel("bounced"),
        FieldPanel("last_emailed", read_only=True)
    ]
    list_display = ["email", "opted_out", "bounced", "last_emailed"]


class SearchLocationViewSet(SnippetViewSet):
    model = SearchLocation
    panels = [
        FieldPanel("type"),
        FieldPanel("name")
    ]
    list_display = ["name", "type"]


class VerticalViewSet(SnippetViewSet):
    model = Vertical
    panels = [
        FieldPanel("name"),
        FieldPanel("pain_points"),
        FieldPanel("description"),
        InlinePanel("search_terms")
    ]
    list_display = ["name"]


class DimensionsViewSetGroup(SnippetViewSetGroup):
    items = (SearchLocationViewSet, VerticalViewSet, EmailViewSet)
    menu_icon = "cog"
    menu_name = "dimensions"
    menu_label = "Dimensions"
