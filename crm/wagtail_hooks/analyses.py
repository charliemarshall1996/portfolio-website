from wagtail.admin.panels import FieldPanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import LighthouseAnalysis


class LighthouseAnalysisViewSet(SnippetViewSet):
    model = LighthouseAnalysis
    panels = [
        FieldPanel("website", read_only=True),
        FieldPanel("created_at", read_only=True),
        FieldPanel("report_url", read_only=True)
    ]
    list_display = ["website__url", "created_at", "report_url"]


class AnalysisViewSetGroup(SnippetViewSetGroup):
    items = [LighthouseAnalysisViewSet,]
    menu_icon = "site"
    menu_name = "analyses"
    menu_label = "Analyses"
