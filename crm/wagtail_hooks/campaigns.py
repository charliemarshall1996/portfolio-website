
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import Campaign


class CampaignSnippetViewSet(SnippetViewSet):
    model = Campaign
    panels = [
        FieldPanel("name"),
        FieldPanel("type"),
        FieldPanel("medium"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("is_active"),
        MultiFieldPanel(
            (FieldPanel("vertical"),
             InlinePanel("campaign_search_locations", label="Locations")),
            heading="Search Parameters"
        ),
        FieldPanel("description")
    ]
    list_display = ["name", "type", "medium", "start_date", "end_date"]


class CampaignsSnippetViewSetGroup(SnippetViewSetGroup):
    items = (CampaignSnippetViewSet,)
    menu_icon = "calendar-alt"
    menu_name = "campaigns"
    menu_label = "Campaigns"
