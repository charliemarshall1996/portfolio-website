
from crm import models
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import InlinePanel, FieldPanel


class OutreachEmailInlinePanel(InlinePanel):
    model = models.OutreachEmail
    extra = 1


class OutreachWebsiteInlinePanel(InlinePanel):
    model = models.OutreachWebsite
    extra = 1


class OutreachViewSet(SnippetViewSet):
    model = models.Outreach
    list_display = ("campaign_search_parameter", "date", "medium")
    panels = [
        FieldPanel("campaign_search_parameter"),
        FieldPanel("date"),
        FieldPanel("medium"),
        OutreachEmailInlinePanel("email", label="Emails"),
        OutreachWebsiteInlinePanel("website", label="Websites"),
    ]


class OutreachViewSetGroup(SnippetViewSetGroup):
    items = [OutreachViewSet, ]
    menu_icon = "mail"
    menu_name = "outreach"
    menu_label = "Outreach"
