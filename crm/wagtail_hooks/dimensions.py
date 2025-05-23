
from crm import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup


class AddressViewSet(SnippetViewSet):
    model = models.Address
    menu_label = "Addresses"
    list_display = ("address_line_1", "town", "postcode")
    panels = [
        FieldPanel("line1"),
        FieldPanel("line2"),
        FieldPanel("town"),
        FieldPanel("region"),
        FieldPanel("postcode"),
        FieldPanel("country")
    ]


class EmailViewSet(SnippetViewSet):
    model = models.Email
    menu_label = "Emails"
    list_display = ("email", "opted_out", "bounced")
    panel = [
        FieldPanel("email"),
        FieldPanel("opted_out"),
        FieldPanel("bounced"),
        FieldPanel("last_emailed", read_only=True)
    ]


class LighthouseAnalysisViewSet(SnippetViewSet):
    model = models.LighthouseAnalysis
    list_display = ("website__url", "created_at", "report_url")
    panels = [
        FieldPanel("website", read_only=True),
        FieldPanel("created_at", read_only=True),
        FieldPanel("report_url", read_only=True)
    ]


class PhoneNumberViewSet(SnippetViewSet):
    model = models.PhoneNumber
    menu_label = "Phone Numbers"
    list_display = ("number", "type")
    panels = [
        FieldPanel("phone_number"),
        FieldPanel("type")
    ]


class SearchLocationViewSet(SnippetViewSet):
    model = models.SearchLocation
    list_display = ("name", "type")
    panels = [
        FieldPanel("name"),
        FieldPanel("type")
    ]


class VerticalViewSet(SnippetViewSet):
    model = models.Vertical
    list_display = ("name",)
    panels = [
        FieldPanel("name"),
        InlinePanel("painpoints"),
        InlinePanel("search_terms")
    ]


class WebsiteViewSet(SnippetViewSet):
    model = models.Website
    list_display = ("url",)
    panels = [
        FieldPanel("url")
    ]


class DimensionsViewSetGroup(SnippetViewSetGroup):
    items = [AddressViewSet, EmailViewSet, LighthouseAnalysisViewSet,
             PhoneNumberViewSet, SearchLocationViewSet, VerticalViewSet, WebsiteViewSet]
    menu_icon = "tasks"
    menu_name = "dimensions"
    menu_label = "Dimensions"
