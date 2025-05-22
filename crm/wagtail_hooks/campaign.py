from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import Campaign


class CampaignViewSet(SnippetViewSet):
    model = Campaign
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
            heading="Conent",
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
