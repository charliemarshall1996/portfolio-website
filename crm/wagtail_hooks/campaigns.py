
from crm import models
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


class CampaignViewSet(SnippetViewSet):
    model = models.Campaign
    panels = [
        FieldPanel("type"),
        FieldPanel("medium"),
        FieldPanel("description"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("is_active"),
        MultiFieldPanel(
            (
                FieldPanel("vertical"),
                InlinePanel("search_locations", label="locations"),
            ),
            heading="Search Parameters",
        ),
        MultiFieldPanel(
            (
                InlinePanel(
                    "email_content", label="Email Content", max_num=5, min_num=5
                ),
            ),
            heading="Content",
        ),
    ]
    list_display = ["start_date", "end_date", "type", "medium", "is_active"]


class CampaignViewSetGroup(SnippetViewSetGroup):
    items = [
        CampaignViewSet,
    ]
    menu_icon = "calendar-alt"
    menu_name = "campaign"
    menu_label = "Campaign"
