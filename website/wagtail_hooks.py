from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
)


class IntervalScheduleSnippet(SnippetViewSet):
    model = IntervalSchedule
    list_display = ("every", "period")
    panels = [
        FieldPanel("every"),
        FieldPanel("period"),
    ]


class PeriodicTaskSnippet(SnippetViewSet):
    model = PeriodicTask
    list_display = (
        "name",
        "task",
        "enabled",
        "last_run_at",
        "total_run_count",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("task"),
        FieldPanel("interval"),
        FieldPanel("args"),
        FieldPanel("kwargs"),
        FieldPanel("enabled"),
    ]


class WebsiteSchedulingSnippetGroup(SnippetViewSetGroup):
    items = (PeriodicTaskSnippet, IntervalScheduleSnippet)
    menu_icon = "calendar-check"
    menu_label = "Website Analysis Scheduling"
    menu_name = "website-analysis-scheduling"


register_snippet(WebsiteSchedulingSnippetGroup)
